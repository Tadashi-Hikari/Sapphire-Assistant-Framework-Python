# Core is the primary router, it should run then hand off to a specialized router if need be
import socketserver, argparse, subprocess, json

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
        print(data)
        post_office(message)

# This is the primary routing service. This kind of looks like parser....
def post_office(message):
    knownroutes = ["nltk-parser.py"]
    if(message["from"] in knownroutes):
        print("It's from the parser")
    else:
        print("Default action")

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
    parser.add_argument('-n', dest='null', help="placeholder command")
    args = parser.parse_args()

    # This is the main thing that needs to run
    # start_server()
    wrap_process("nltk-parser.py")

