# Core is the primary router, it should run then hand off to a specialized router if need be
import socketserver, argparse, subprocess

# This is the UDP server. It's the basis for listening to incoming messages
class CoreUDPHandler (socketserver.BaseRequestHandler):
    def handle(self):
        #notify("Some data was recieved!")
        data = self.request[0].strip()
        socket = self.request[1]
        #notify("{} wrote:".format(self.client_address[0]))
        data = data.decode('utf-8')
        # I think this is a selflib command
        #message = deserialize(data)
        # This is where the BULK routing happens
        print(data)
        #post_office(message)

# This is the primary routing service. This kind of looks like parser....
def post_office(message):
    if ("weather"):
        print("weather")
    elif ("lights"):
        print("lights")
    elif ("note"):
        print("note")
    elif ("vlc"):
        print("vlc")
    else:
        return 1

# This should call udp-client, but I need to configure a buffer for streaming data, like the STT
def wrap_process(process):
    command = ["python3",process,"wake me up at ten"]
    ps = subprocess.Popen(command,stdout=subprocess.PIPE)
    subprocess.check_output(["python3","udp-client.py","-t",process], stdin=ps.stdout)
    ps.wait()
    # This should be printing it's STDOUT to the server handler

def start_server():
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST,PORT), CoreUDPHandler) as server:
        server.serve_forever()

if __name__ == '__main__':
    # This is the main thing that needs to run
    # start_server()
    wrap_process("nltk-parser.py")

