import selflib, argparse
from selflib import *

def format_for_commandline(message): # I don't like sending the whole message... or was that the point...?
    # notify("serialized: %s"%(message))
    msg = deserialize(message)
    payload = msg['payload'] # get the payload

    print("formatter payload: %s"%(payload))
    
    command = ['-t','command_variables','-l'] # this needs to be more nuanced. Get 'command' where 'variables' match
    response = call_database(command) # query for the tables flags & variables
    text = response.decode('utf-8')
    records = deserialize(text)

    comm = []
    for record in records: # this is brittle. I don't like it
        if record['command'] == payload['label'] and record['variable'] in payload: #msg['name'] is what?
            comm.append(record['location'])
            break
    
    for i,record in enumerate(records): # for variable:flags in database
        for j,other in enumerate(records[i+1:]):
            if record['command'] == other['command']:
                records.pop(j)
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
