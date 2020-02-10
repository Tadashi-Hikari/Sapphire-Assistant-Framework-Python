import argparse, selflib, subprocess, sys, configparser
from padatious import IntentContainer
from selflib import *

# Global variables
container = IntentContainer('intent_cache') # this is where the trained NN stuff is saved
# change stdout since padatious is noisy. This can be changed w/ verbose
stdout = sys.stdout # keep a local copy
sys.stdout = None
#CONFIG = 
command_table = "commands"
training_utterances_table = "utterances"

''' I need to have padatious running as a service, due to its need to load intents every time the program is initialized. Likewise, I need to have padatious pull from the database, rather handwriting the add_intent each time. '''

def load_config(): # this is not enabled yet
    config = configparser.ConfigParser() 
    config.read(CONFIG) # this needs to be implemented with a try/catch

    command_table = "commands"
    trianing_utterances_table = "utterances"

def parse(utterance):
    notify("Running parser")
    data = container.calc_intent(utterance)
    notify("data name: %s"%(data.name)) # name of matched command
    notify("data match: %s"%(data.matches)) # list of matched variables

    format = {}
    format['label'] = data.name # <- this should be payload...? does this give too much detail about implementation? or is this just protocol?
    format.update(data.matches) # these are each found variable, which is their own kvp. this should iterate over...

    notify(format)
    serial = serialize(format)
    sys.stdout = stdout
    if data.conf >= .5: # it should match names. but padatious always returns something
        print(serial) # This is returning the data over cli. should I not serialize?
        # call_application(["command-formatter.py","-f",serial]) # <- This should actually return to core
    else:
        serial = serialize("No matches")
        notify("Confidence: %d"%(data.conf))
        print(serial) # maybe change this to match a 'no match' command
    # print(data)

def train(): # I need to find a way to supress the output of this..
    command = ["-t", command_table, "-l"] # list all the commands in the database <- this should load from a configurable database...
    print("calling database")
    data = call_database(command)
    records = deserialize(data) # records are a list[dict{}] structure. each dict is a record

    notify(records)
    
    command = ["-t", training_utterances_table, "-l"] # list all the utterances in the database <- new file doesn't name commands <- this should load from a configurable database...
    data = call_database(command)
    utterances = data.decode('utf-8')
    utterances = utterances.strip()
    utterances = deserialize(utterances)
    notify(utterances) 
    
    for record in records: # records is a list, record is a dict. records of commands
        record["utterances"] = []  # <- why am I clearing this here? If it's not cleared, then it doesn't make a new record, it just keeps referencing the same memory location. 
        # if it's new new, then also load the utterances
        for i,utterance in enumerate(utterances): # for every utterance in the database...
            if utterance["command"] == record["alias"]: # check if the utterance matches a known command program alias. If this crashes, make sure the csv column headers match
                record["utterances"].append(utterance["tagged"]) # add the utterance of the know command to the list                loud_notify("APPENDING UTT",utterance["utterance"])
                # utterances.pop(i) # get rid of THAT SPECIFIC RECORD in utterances. Don't get rid of the command. I don't think I can use this, cause it throws off the enumerate

        loud_notify("RECORD",record)
        container.add_intent(record["command"], record["utterances"], True)
    # container.train()    notify("Training")
    container.train()

def example():
    container = IntentContainer('intent_cache')
    container.add_intent('hello', ['Hi there!', 'Hello.'])
    container.add_intent('goodbye', ['See you!', 'Goodbye!'])
    container.add_intent('search', ['Search for {query} (using|on) {engine}.'])
    container.train()
   
    print(container.calc_intent('Hello there!'))
    print(container.calc_intent('Search for the cats on CatTube.'))

    data = container.calc_intent('Search for the cats on CatTube.')
    print(data.name)
    print(data.sent)
    print(data.matches)
    print(data.conf)
    
    container.remove_intent('goodbye')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="An intent parsing service, using padatious")
    parser.add_argument('-v', dest='verbose', help="make core verbose", action='store_true')
    parser.add_argument('-p', dest='parse', help="enter the text to parse")
    parser.add_argument('-e', dest='example', help="display the example", action='store_true')
    args = parser.parse_args()

    if args.verbose is True:
        selflib.verbose = True
        sys.stdout = stdout
    
    #init() # load the entire cache into the parser.
    #load_config()
    train()
    
    if args.example is True:
        example()

    if args.parse is not None:
        parse(args.parse)
