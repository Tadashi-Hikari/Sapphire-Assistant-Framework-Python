import argparse, subprocess, socket, json, io, os, notify2

verbose = False

def get_metadata_id_from(meta): # meta is a user/application definable metapackage
    data = call_application(meta) # application meta will create a timestamp entry of the relavent metadata, and then pass back the id number to log in the database
    id = data.decode('utf-8')
    return id

def user_notify(message): # message string, not message like the protocol
    notify2.init('Assistant')
    n = notify2.Notification("Notification",
                             message,
                             "notification-message-im" # Icon name
                             )
    n.show()

def call_database(flags): # is this too specific to sql? it could be an important distinction for de/serial purpose
    COMMAND = os.getenv("ASST_COMMAND")
    database = os.getenv("ASST_DATABASE")
    
    command = [COMMAND,database]
    for item in flags:
        command.append(item)
    notify(command)
    process = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE) # the returned value
    if process.returncode is not 0:
        notify("The following command returned a non-zero code: %s"%(command))
        notify("RETURN CODE: %d"%(process.returncode))
        notify("STDERR: %s"%(process.stderr))
    data = process.stdout
    return data # it is returned, since selflib is part of the program, not called over command line why doesn't this return stdout?

def call_application(flags): # this can be put into call_database, but I don't need it to call env variables again. is this bad?
    COMMAND = os.getenv("ASST_COMMAND")
    database = os.getenv("ASST_DATABASE")
    notify("COMMAND: %s"%(COMMAND))
    notify("DATABASE: %s"%(database))
    
    notify("call_application called. calling %s"%(flags))
    command = [COMMAND]
    for item in flags:
        command.append(item)
    process = subprocess.run(command,stdout=subprocess.PIPE)
    data = process.stdout # Don't decode. This could allow for binary responses with graphics, etc
    return data # this data is returned, since this is a library called within an application. should have a unxi sample program built in

def message_server(data): # isn't this exactly what I am looking to do w/ call_application?
    # Send the information to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(data + "\n", "utf-8"), ("localhost", 9999)) 

def notify(string):
    if verbose == True:
        print(string)

def loud_notify(tag, string):
    if verbose == True:
        print("---START "+tag+"---")
        print(string)
        print("---END "+tag+"---")

def serialize(message):
    data = json.dumps(message)
    return data

def deserialize(data):
    message = json.loads(data)
    return message

def read_config_file():
    print("This feature is not yet setup")
    
# run a core associated component. deserialize so it can be networked. 
def run_with_return(command): # commands structure is a list. ["python3","program.py","-s","someinput"] broken up into atoms, rather than a long string. It could just be "python3 program.py -s someinput"] though...
    loud_notify("Running Component", command)
    pipe = pipes.Template()
    f = pipe.open('pipefile','w')
    subprocess.run(command, stdout=f)
    f.close()
    f = pipe.open('pipefile','r')
    string = f.read()
    return(deserialize(string))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="main udp server and router")
    parser.add_argument('-v', dest='verbose', help="print verbose output", action='store_true')
    parser.add_argument('-d', dest='deserialize', help="deserialize string input")
    parser.add_argument('-s', dest='serialize', help="deserialize string input")
    args = parser.parse_args()

    if args.verbose is True:
        verbose = True

    if args.deserialize is not None:
        deserialize(args.deserialize)

    if args.serialize is not None:
        serialize(args.serialize)
