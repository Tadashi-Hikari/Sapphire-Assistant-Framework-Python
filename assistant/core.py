import subprocess, socketserver, socket, argparse, re, os, selflib, pipes, time, configparser
from multiprocessing import Process
from selflib import *

# These values are set in load_config, from the values in selflib.py. just here for global reference. Maybe move to main?
COMMAND = "python3"
base = "/home/chris/Lab/dex-framework/" # Well. This needs to be scrubbed... what should it be?
stt = base+"sphinx-server.py"
PARSER = base+"padatious-parser.py" # this conflicts w/ arg parser. be careful changing it
version = "0.0.1"
database = base+"sqldatabase.py"
formatter = base+"command-formatter.py"
gui = base+"gui"
CONFIG = "~/.config/assistant/core.conf" # <- The config directory should probably be broadcast
LOG_DIR = "/var/log/assistant/"

# this is the pipeline the message goes through. to hack this, just inject a small method that checks the current spot in the path and injects your custom command
message_path = ["parser","command-formatter","command"] # you can hack in extra modules here if you'd like

''' To have assistant handle non text data (such as audio or pictures), just stdout pipe the binary form into message, and give it a custom component tag to run'''

class AssistantUDPHandler(socketserver.BaseRequestHandler):
    # This is the handler function. it must be polling somehow <- The server is an endless loop
    def handle(self):
        notify("Some data was recieved!")
        data = self.request[0].strip() # remove that trailing '\n' that is added for some reason...
        socket = self.request[1]
        notify("{} wrote:".format(self.client_address[0]))
        notify(data)
        
        data = data.decode('utf-8')
        message = deserialize(data) # this throws error for non kvp data. if it's untagged, it puts it in... [original]
        loud_notify("MESSAGE", message) #<- this is where the message is coming from...
        
        post_office(message) # Determine where the message should go from here

def log_and_tag(message):
    # tag original data
    # log original data
    message["original"] = message["payload"] # this may be redundant, since it's also the first in the chain
    message["id"] = 1 # but actually, it should generate a new ID based on the table its being logged into
    logger = Process(target=log,args=(message,))
    logger.run()
    return message
        
def post_office(message): # this is the primary routing service
    # I can expect it to be 
    notify("sorting in the post office")
    
    # verify id
    if 'id' not in message: # if its a new message, it also ensures that it's in proper format
        message = log_and_tag(message)
    
    # Do I want these to run independently? Or only perform one function. 
    if 'core' in message:
        print("System functions not yet implemented")
    elif 'custom' in message and message['custom'] is not None: # a custom hook. have it run a custom post_office here
        print("Doing something custom")
    elif 'fallback' in message: # this shouldn't be explicit, per se....
        print("Fallback wouldn't be in message. It should be what happens if no parse is found")        
    elif 'from' in message and message['from'] in message_path: # if it came from the core, and is not a new prompt 
        # if 'chain' in message: # this is where I add the chain logic
        if message['payload'] == "No matches" and message['from'] == "parser": 
            user_notify("Message: \"%s\" does not match a command"%(message['original']))
        elif message['from'] == parser: # I don't like how this is all being evaluated here. perhaps post_office() should be moved out to a separte file
            serial = serialize(message)
            command = [formatter,"-f",serial,"-v"]
            data = call_application(command)
            response = data.decode('utf-8')
            print(response)
        else:
            user_notify("Payload: %s. It appears we have reached the end"%(message["payload"]))
            print("It appears we have reached the end")
    else: # This sends the utterance to the parser. What happens after it's parsed? format for cli, and run program.
        notify("Unsure what to do, sending to %s"%(message_path[0])) # send it from the start of the pipeline
        message['from'] = message_path[0] # append the parser tag to the to/from
        command = [PARSER,"-p",message['payload']]
        notify("Sending this command: %s"%(command))
        notify("%s: %s"%(message_path[0],PARSER))
        notify("MESSAGE: %s"%(message['payload']))
        payload = call_application(command).decode('utf-8')
        message['payload'] = deserialize(payload)
        notify(message['payload'])
        serial = serialize(message)
        # check for next step in config?
        message_server(serial)
        
def log(message): # Later, perhaps... check how inefficient this may be. Also it's not robust
    notify("logging %s"%(message))
    META_ID = "meta_id"
    #meta_id = get_metadata_id_from("metadata") # oh shit, I don't think I need this here
    meta_id = 1
    table = "logged_input" # moving this up, so it can be overwritable
     
    # Check if the table exists. I can change this so [core] allows for different databases
    notify("Checking if table %s exists"%(table)) # this needs to be less hardcoded
    command = ["-chk",table]
    data = call_database(command)
    response = data.decode('utf-8')
    
    # this is a bit hardcoded for a flexable logger
    if 'False' in response: # if response == "False" wasn't working. this does
        notify("The table does not exist")
        # headers = get_utt_id() # this gets the unique_id from the table
        # headers += utterance 
        # headers += get_meta_id() # this gets metadata for the specific table
        headers = "utterance" # <- needs meta_id generated. metas primary key
        command = ["-t",table,"-c",headers] # utterance needs to be replace w/ config check. this is failing because it needs data to input?
        call_database(command) # I am not worried about the callback
        command = ["-t",table,"--link-metadata"]
        call_database(command) #this is just added in. I could probably just directly link it. I may need a logic change, but this is generic to add to a table later

    data = "%s,%s"%(message["payload"],meta_id) # This uses the earlier generated meta_id
    # this is actually an enter-and-get-id for the metadata, so I can put the foreign key in the new slot
    notify("Sending data to sqldatabase: %s"%(data))
    command = ["-t", table, "--insert-and-get-id", data] # I am getting this ID, because it will be used as the message['id']
    data = call_database(command)
    id = data.decode('utf-8').strip() # the message['id']
    message["id"] = id
    # insert the data into the table that I just expanded....? that should just be metadata... oh! Its only adding data
    #text_command = "INSERT %s IN %s WHERE ID = %d"%(data,table,int(id)) # I need to make this a built in command
    #command = ["-t", table, "--text", text_command]
    #call_database(command)
    notify("Logged %s"%(message["payload"]))

def load_config(): # using configparser
    config = configparser.ConfigParser()
    
    try:
        config.read('.assistantrc')
    except:
        notify("There doesn't seem to be a config file...")

    os.environ["ASST_DATABASE"] = database # set this externally for other programs to see
    os.environ["ASST_BASE"] = base
    os.environ["ASST_COMMAND"] = COMMAND
    os.environ["ASST_CONFIG"] = CONFIG
    notify("config loaded")

def start_ui(): # You should be a separate process, that listens over the network, and interacts with components over its own shell
    subprocess.Popen(["python3",gui]) # This doesn't interact w/ core once started
    # Perhaps it DOES interact with core. I just haven't built it yet

def start_stt(): # You should be a separate process that sends things over the network
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # make the socket look like a file
    sock.connect(("localhost",9999))
    pipefile = sock.makefile('w') # this should be in memeory only. change it to IOFile or something
    command = [COMMAND,"sphinx-server.py","-d"]
    subprocess.run(command, stdout=pipefile) # this is a special case, as a daemon its always talking to core.
    # This should be printing it's STDOUT to the server handler
    
def start_applications(): # run at the start of core.py
    notify("Starting applications")
    # start_ui() # start the user iterface
    # notify("Started UI")
    # start_parser() # parser needs to be a service, due to how padatious loads/trains
    # notify("Started Padatious")
    # start_stt()
    # notify("Started STT")

def install():
    # run the bash script for setting up assistatn
    shell_out("./setup-database")
    
def get_record(name): # returns a record in dict format
    return run_component([COMMAND,LOOKUP,'-q',name])
    
def stop_applications():
    notify("Stopping applications")

def edit_utterances(): # load a csv file in libreoffice calc to edit. probably will move this out of core
    command = [COMMAND,database,"-wc","-t","utterance"]
    filename = subprocess.run(command, stdout=subprocess.PIPE)
    filename = filename.stdout.decode('utf-8')
    os.system("libreoffice --calc -o %s"%(base+filename)) # I need this to trigger an update on next load
    
def shell_out(filename): # Drop to the editor, for editing core scripts
    os.system("emacs %s"%(filename))

def send_over_network(command): # this is just a basic UDP client
    # this sends an untagged message to core. how is it handled...
    time.sleep(1) # wait until the server has joined the main process.
    host, port = "localhost", 9999
    data = command
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(data + "\n", "utf-8"), (host, port))
    
def start_server(): # Start UDP server
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST,PORT), AssistantUDPHandler) as server:
        server.serve_forever()

if __name__ == '__main__':    # Main program loop
    parser = argparse.ArgumentParser(description="main udp server and router")
    parser.add_argument('-c', dest='command', help="enter a textual command (as if spoken)")
    parser.add_argument('-v', dest='verbose', help="make core verbose", action='store_true')
    parser.add_argument('-i', dest='install', help="install a command", action='store_true')
    parser.add_argument('-u', dest='utt', help="edit stored utterances", action='store_true')
    args = parser.parse_args()
    
    if args.verbose == True:
        selflib.verbose = True

    load_config()
    start_applications() # I need the net_server object, since this becomes the main program. SocketServer UDP runs in its own thread, I suppose (keep an eye out for memory leaks)

    # Set up how to handle command line switches. Maybe I need to queue these up..?
    if args.install == True: # this may need to be changed if core is the server
        install()
        exit()

    if args.utt is True:
        edit_utterances()

    if args.command is not None:
        message = {}
        
        message['payload'] = args.command
        serialized = selflib.serialize(message)
        send_internal = Process(target=send_over_network, args=(serialized,), daemon=True)  # this doesn't seem to be running separate
        send_internal.start() # this is daemonized so that net_server displays it in stdout

    notify("Starting Web Server")
    start_server()
