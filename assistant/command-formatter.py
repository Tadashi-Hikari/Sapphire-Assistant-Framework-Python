import selflib, argparse
from selflib import *

''' I am running into an issue here where the parser is slecting an action, but doesn't specify what command it is for '''

def format_for_commandline(message):
    msg = deserialize(message)
    payload = msg['payload'] # get the payload, which is currently a padatious response

    print("THE INCOMING MESSAGE IS AS FOLLOWS: ",msg)
    
    sort_column = "placement"
    command_table = "commands"
    alias = "command"
    
    # get the command base, get all commands sorted by #. This makes sure commands come out int the proper order
    #sqlcommand = 'SELECT * FROM %s WHERE %s = "%s" ORDER BY CAST(%s AS INT)'%(command_table, alias, payload["label"], sort_column) # this is SUUUPER database specific. get the commands for the alias. sort they by priority
    # should this be alias, or flag. I want it to match the specific command, as decided by the parser
    sqlcommand = 'SELECT * FROM %s WHERE %s = "%s" ORDER BY CAST(%s AS INT)'%(command_table, alias, payload["label"], sort_column)
    command = ['-t','commands','--text',sqlcommand] # this is changed to the commands table. --text allows sql to take string inputx
    response = call_database(command) # query for the tables flags & variables
    text = response.decode('utf-8')
    records = deserialize(text)

    print("THE RECORDS ARE AS FOLLOWS: %s"%(records)) # the records are returning as a list, not a kv dictionary. This is an issue
    print("THE PAYLOAD IS AS FOLLOWS: %s"%(payload))

    # for the sake of making things more readable
    unique_id = 0
    alias = 1
    base = 2
    command = 3
    flag = 4
    placement = 5
    prefix = 6 # Prefix means that it needs to be prefaced?
    converter = 7
    link = 8
    
    comm = [] 
    for record in records: # populate with the 1
        if int(record[prefix]) == int(1): # typecast, since it's gonna be a string
            comm.append(record[base]) # I def need to rework this logic. what if the base is different for something else?
            #comm.append(record[alias]) # why is this needed?
            if record[flag] is not "None":
                comm.append(record[flag])

    for record in records: # populate with the 0s
        if record[command] in payload and int(record[placement]) == 0: # command is placeholder for variable too, should I change the table? logic?
            if record[flag] is not "None":
                comm.append(record[flag])
            comm.append(payload[record[flag]]) # this works cause flag is a standin for variable

    # damn, think this through. It's an ideal situation for recursion
    for i,record in enumerate(records,2): # count through the number of records, and index++ each time. this could be a source of slowdown, btw, and it won't catch numbers past a natural increment
        if record[command] in payload and int(record["placement"]) == i:
            if record[flag] is not "None":
                comm.append(record[flag])
            command.append(payload[record])       
    
    print("command: ",comm)

def format_for_commandline2(message): # I don't like sending the whole message... or was that the point...?
    # I want to recieve:
    # - The alias/base for the selected command
    # - The commands themeselves
    # - the related variable for the command.

    # SELECT * FROM commands WHERE alias = "calendar" AND command = "add" OR command = "end" ORDER BY CAST(placement AS INT)
    get(records where alias == base && command == x,y,z sorted by priority(num)
    for numInCommands:
        if num == 0:
          str = "%s=%s"
        str += "OR %s=%s"

    for eachRecord in records:
        if num == 0:
          command = record['base']
        if record['flag'] != none:
          command += record['flag']
        command += payload['variable'] # how do I identify the variable, if it's not in the command database

    print(command)
    #run(command)
                                
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="format padatious output to cli")
    parser.add_argument('-v', dest='verbose', help="make application verbose", action='store_true')
    parser.add_argument('-f', dest='format', help="enter the text to format")
    args = parser.parse_args()

    if args.verbose is True:
        selflib.verbose = True

    if args.format is not None:
        format_for_commandline(args.format)
