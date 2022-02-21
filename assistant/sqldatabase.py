#!/usr/bin/python3
import selflib, argparse, sqlite3, os
from selflib import *

''' Every database that gets made for sqlite is assumed to have an ID column for it's own primary key. If this is not the case, just ignore it when getting results. '''

''' This program needs to be turned into a server w/ queue, or it needs to be converted to postgresql from sqlite3, in order to handle queuing '''

database = os.getenv("ASST_HOME") # These need to always be held, per component
if database == None:
    notify("make the directory for this. For now, I don't want to pollute the devs computer")
    #database = "~/.local/assistant/"
database="core.db" # this should probably be standardized. Append it to the prior directory when change is made

table = "main" # same

# --- START OF UNIVERSAL COMMANDS ---
# This is only useful I am calling sqldatabase as a library

def set_database(db):
    global database
    database = db

def set_table(t):
    global table
    table = t[0]

# --- START OF DYNAMIC DATABASE COMMANDS (CUSTOM) ---

# The logic for this is the same as adding a columnt to any table, in cause that needs to be added in
def link_to_the_metadata(): # this is really just adding a column
    META_ID = "meta_id" # If you hate this table header name, change it here

    command = "ALTER TABLE %s ADD COLUMN %s TEXT"%(table,META_ID)
    c.execute(command)

def rename_table():
    command = "ALTER TABLE %s RENAME TO %s"
    
def enter_and_get_id(entries):
    add_entry(entries)
    id = c.lastrowid # because they use INTEGER PRIMARY KEY, the rowid and ID column are the same
    print(id)
    
def outer_join(cols,from_table,to): #join all rows, and all columns (cartesian product of records)
    # placeholder = "CREATE TABLE %s AS SELECT * FROM %s LEFT OUTER JOIN %s" # this makes a new table
    print("Work in progress")

# --- START OF STANDARD SQL COMMANDS ---
def create_table(columns): # Build this up
    columns=columns.strip() # remove needless whitespace
    split_line=columns.split(",")
    headers = "id INTEGER PRIMARY KEY" # every table has this ID anyway. I am just making it accessible. See: https://www.sqlite.org/rowidtable.html 2.0 Quirks
    for segment in split_line:
            headers+=",%s TEXT"%(segment) # you can always assume it will start w/ the ID column

    command="CREATE TABLE %s (%s)"%(table,headers)
    c.execute(command)
    # entry is basically CSV for each column

def drop_table(table):
    command="DROP TABLE IF EXISTS %s"%(table)
    c.execute(command)
    
def add_entry(line):
    headers=get_column_names() # get_column_names doesn't return the ID column
    headers_list = headers.split(",")
    headers = ""
    for i,header in enumerate(headers_list):
        if i is 0:
            continue
        if i is 1:
            headers += "%s"%(header)
        else:
            headers += ",%s"%(header)
    
    notify(headers)

    line_arr = line.split(",")
    line = "" # maybe make this nicer?
    for i,entry in enumerate(line_arr):
        entry = entry.strip()
        if i is 0:
            line+="\"%s\""%(entry) # put quotes around the data
        else: 
            line+=",\"%s\""%(entry) # put quotes around the data

    command="INSERT INTO %s(%s) VALUES(%s)"%(table,headers,line) #it's already set up for sqlite)
    notify("COMMAND: %s"%(command))
    c.execute(command)

def get_column_names():
    command="PRAGMA table_info(%s)"%(table) # Get the column names. table is a global var
    c.execute(command)
    raw_table_info=c.fetchall()
    column_names = ""
    
    for i,row in enumerate(raw_table_info):
        if i is 0:
            column_names+="%s"%(row[1]) # why is it row[1] and not just row? cause raw_table_info gives an array of data, and row[1] contains one header name per row
        else:
            column_names+=",%s"%(row[1]) # get the column name

    notify("COL NAMES: %s"%(column_names))
    return column_names # return col names, formatted as 'string,...,string'

# basically one line per record CSV
def batch_add_entryf(entries):
    for entry in entries:
        add_entry(entry)
    
def take_text_input(text):
    # this could be dangerous if network facing...
    try:
        c.execute(text)
        print(c.fetchall())
    except sqlite3.Error:
        print(sqlite3.Error)
    exit()
    
def list_table(): # This sends a list of KVP, for deserialize
    headers = get_column_names()
    command = "SELECT * FROM \'%s\'"%(table)
    record_list = []

    headers = headers.split(',') # get_column_names hands them back as a single string
    c.execute(command)
    database_records = c.fetchall()

    for i,record in enumerate(database_records):
        formatted_record = {} # needs to be generated in loop as factory, else its a ref to the same record
        for j,entry in enumerate(record): # print each individual entry
            formatted_record[headers[j]] = entry # add each entry to kvp record
        record_list.append(formatted_record) # add the kvp record

    loud_notify("RECORD LIST", record_list)
    serialized = serialize(record_list)
    if args.write is not True:
        print(serialized) # <- this is for use in depreciated-core.py
    return serialized # <- this is for internal sqldatabase useage (and selflib)

def list_all_tables():
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(c.fetchall())
    exit()
    
def query_table(key):
    command="SELECT %s FROM %s"%(key,table)
    c.execute(command)
    results = c.fetchall()
    print(results)
    
def create_table_from_csv(file_name):
    #open_file = open(file_name,"rb") # I am fairly certain I have this working from a bytes array to work from the command line. I don't think I need it to...
    open_file = open(file_name,"r")
    file_data = open_file.readlines()
    
    for i,line in enumerate(file_data):
        if i is 0:
            notify(line)
            create_table(line)
        else:
            notify("ADDING LINE: %s"%line)
            add_entry(line)

def load_from_csv(file_name): # this can probably just be moved elsewhere w/ a try/catch
    open_file = open(file_name,"rb")
    file_data = open_file.readlines()
    
    for line in enumerate(file_data): # add all the data
        add_entry(line) # this is just the line

def write_to_csv(): # write a table to a csv file, and return the filename
    # this is pulling from the database and writing to a file. Should it write to the file? should it pull from the database?
    serialized = list_table() # this is an issue. since they print, they're not designed for internal use
    records = deserialize(serialized)
    # Add a file selection mechanism
    filename = "prep-csv/utterance-csv" # the training utterances, which is separate from the log (why?)
    
    f = open(filename, "w") # this shouldn't be so static, should it?
    
    for j,record in enumerate(records): # this loop is very brittle
        if j == 0: # if it's the very first entry, print the headers
            for i,entry in enumerate(record): # same loop as below, just for headers
                if i == 0:
                    f.write(entry)
                else:
                    f.write(",%s"%(entry))
            f.write('\n')
        for i,entry in enumerate(record.values()):
            if i == 0:
                f.write(entry)
            else:
                f.write(",%s"%(entry))
        f.write('\n')

    f.close()
    print(filename)
    
def check_if_table_exists(tableName):
    try:
        command = "SELECT name FROM sqlite_master WHERE type='table' AND name=\'%s\'"%(tableName)
        c.execute(command)
        catch = c.fetchone()
    except sqlite3.Error:
        print("Some kind of SQL error occured")
        print("False") # it wasn't displaying an output for a CLI
        return False
    if catch == None:
        print("False")
        return False
    print("True")
    return True

# --- START OF MAIN PROGRAM LOGIC ---
if __name__ == '__main__':

    ''' I am thinking this whole section could use a lot of work. AT LEAST in terms of readability, but perhaps even reducing switches, or at least having them make more sense '''

    parser = argparse.ArgumentParser(description="A simple database manager")
    parser.add_argument('-v', dest='verbose', help="make installer verbose", action='store_true')
    parser.add_argument('-d', dest='database', help="specify database to use")
    parser.add_argument('-t', dest='table', help="specify table to use", nargs=1)
    parser.add_argument('-a', dest='add_sql', help="add an entry to an sql table")
    parser.add_argument('-ac', dest='add_from_csv', help="add entries to an sql table from a csv file")
    parser.add_argument('-c', dest='create_table', help="create an sql table")
    parser.add_argument('-cc', dest='create_csv', help="create an sql table from a csv file") # this can probably be replaced w/ an open try/catch
    parser.add_argument('-wc', dest='write', help="create an sql table from a csv file", action="store_true")
    parser.add_argument('-l', dest='list_table', help="list the data in an sql table", action="store_true")
    parser.add_argument('-la', dest='list_all', help="list all sql tables", action="store_true")
    parser.add_argument('-dt', dest='drop', help="drop an sql table")
    parser.add_argument('-com', dest="command", help="Enter an SQL command from the command line")
    parser.add_argument('-chk', dest="check_if_exists", help="check if table exists")
    parser.add_argument('-q', dest="query", help="query an sql table for a certain key")
    parser.add_argument('--link-metadata', dest="meta", help="add a column for metadata id to a table", action="store_true")
    parser.add_argument('--text', dest="text", help="pass text as an sql command")
    parser.add_argument('--insert-and-get-id', dest="enter_and_get", help="enter and get id") # this is meant for getting a foriegn key to give to another table
    
    args = parser.parse_args() # parse the command line arguments
    
    if args.verbose == True: # verbose switch. uses selflib
        selflib.verbose = True

    # these two set internal variables
    if args.database is not None: # establish which file to use
        set_database(args.database)

    conn = sqlite3.connect(database) # gotta init the database before doing anything. if no file exists, maybe I should security check here
    c = conn.cursor()

    if args.table is not None: # establish which table to use
        set_table(args.table)

    # put cli switches here
    if args.create_table is not None: # supply with initial values
        create_table(args.create_table)
    
    if args.create_csv is not None: # this should come before add_from_csv in case somebody appends a second file afterwords
        create_table_from_csv(args.create_csv)
        
    if args.add_from_csv is not None:
        load_from_csv(args.add_from_csv)

    if args.list_table is True:
        list_table()

    if args.add_sql is not None:
        add_entry(args.add_sql)

    if args.list_all is True:
        list_all_tables()

    if args.command is not None:
        take_text_input(args.command)

    if args.drop is not None:
        drop_table(args.drop)

    if args.enter_and_get is not None:
        enter_and_get_id(args.enter_and_get)
        
    if args.check_if_exists is not None:
        check_if_table_exists(args.check_if_exists)

    if args.query is not None:
        query_table(args.query)

    if args.write is True:
        write_to_csv()

    if args.text is not None:
        take_text_input(args.text)
        
    if args.meta is True:
        link_to_the_metadata()
    
    conn.commit()
    conn.close()
