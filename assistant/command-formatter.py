import selflib, argparse
from selflib import *

def format_for_commandline(message): # I don't like sending the whole message... or was that the point...?
    # notify("serialized: %s"%(message))
    msg = deserialize(message)
    payload = msg['payload'] # get the payload

    # if I recall correctly, there was an issue here with using JSON rather than my custom parser

    print("formatter payload: %s"%(payload))
    
    command = ['-t','commands','-l'] # this needs to be more nuanced. Get 'command' where 'variables' match
    response = call_database(command) # query for the tables flags & variables
    # text = response.decode('utf-8') # not needed, cause it's not coming over UDP
    records = deserialize(text)

    # I need ti implement the placement logic
    
    comm = []
    for record in records: # this is brittle. I don't like it
        if record['command'] == payload['label']:
            if record['flag'] in payload and record['flag'] is not "None":
                com.append(record['flag'] 
            comm.append(record['base']) # append the actual shell command to call
            break
    
    for i,record in enumerate(records): # for variable:flags in database
        for j,other in enumerate(records[i+1:]):
            #if record['command'] == other['command']: # this was to speed up the loop. Don't prematurly optimize
               # records.pop(j)
        if record['variable'] in payload and record['command'] == payload['label']: # if the variable type from the db is in the msg from padatious
            comm.append(record['flag'])
            comm.append(payload[record['variable']])

    print("command:",comm)
    #response = call_application(comm) # this is going to return the binary data. What to do with it? I guess ignore it for now..
    print("it works")
                                
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="format padatious output to cli")
    parser.add_argument('-v', dest='verbose', help="make application verbose", action='store_true')
    parser.add_argument('-f', dest='format', help="enter the text to format")
    args = parser.parse_args()

    if args.verbose is True:
        selflib.verbose = True

    if args.format is not None:
        format_for_commandline(args.format)
