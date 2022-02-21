# Core is the primary router, it should run then hand off to a specialized router if need be
import socketserver, argparse, subprocess, json, os, multiprocessing

version = "0.1.0"

# This is the UDP server. It's the basis for listening to incoming messages
class CoreUDPHandler (socketserver.BaseRequestHandler):
    def handle(self):
        #notify("Some data was recieved!")
        data = self.request[0].strip()
        socket = self.request[1]
        #notify("{} wrote:".format(self.client_address[0]))
        data = data.decode('utf-8')
        # I think this is a selflib command
        message = json.loads(data)
        # This is where the BULK routing happens
        #print(data)
        file = open("assistant.log","a+")
        file.write(data)
        file.write("\n")
        file.close()
        post_office(message)

# This is the primary routing service. This kind of looks like parser..
def post_office(message):
    knownroutes = ["nltk-parser.py"]
    if(message["from"] in knownroutes):
        print("It's from the parser")
    else:
        print("Default action")

def run_start_services():
    print("Nothing")
    file = open("start.conf",'r')
    for line in file:
        shell_out(line)

def shell_out(program):  # Drop to the editor, for editing core scripts
    process = subprocess.Popen(["python3",program,"-s"],stdout=subprocess.PIPE)
    print(process.pid)

def wrap_process(process):
    command = ["python3",process,"wake me up at ten"]
    ps = subprocess.Popen(command,stdout=subprocess.PIPE)
    subprocess.check_output(["python3","udp-client.py","-t",process], stdin=ps.stdout)
    ps.wait()

def start_server():
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST,PORT), CoreUDPHandler) as server:
        server.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="main udp server and router")
    parser.add_argument('-s', dest='server', help="start the UDP server",action="store_true")
    parser.add_argument('-t', dest='test', help="start the UDP server",action="store_true")
    args = parser.parse_args()

    # This is demo code
    if(args.test == True):
        shell_out("core-redux.py")
    elif(args.server == True):
        start_server()
        # subprocess.run(["python3","core-redux.py","-s"])
    else:
        wrap_process("nltk-parser.py")

