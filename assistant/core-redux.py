# Core is the primary router, it should run then hand off to a specialized router if need be
import socketserver, socket

# This is the UDP server. It's the basis for listening to incoming messages
class CoreUDPHandler (socketserver.BaseRequestHandler):
    def handle(self):
        notify("Some data was recieved!")
        data = self.request[0].strip()
        socket = self.request[1]
        notify("{} wrote:".format(self.client_address[0]))
        data = data.decode('utf-8')
        # I think this is a selflib command
        message = deserialize(data)
        # This is where the BULK routing happens
        post_office(message)

# This is the primary routing service
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

def start_server():
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST,PORT), CoreUDPHandler) as server:
        server.serve_forever()

if __name__ == '__main__':
    # This is the main thing that needs to run
    start_server()
