import socket, sys, json, argparse

HOST, PORT = "localhost", 9999

parser = argparse.ArgumentParser(description="main udp server and router")
parser.add_argument('-t', dest='title', help="enter a textual command (as if spoken)")
args = parser.parse_args()

# read stdin, as opposed to the command-line options
data = sys.stdin.read()
#" ".join(sys.argv[1:])

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = {}
if(args.title == None):
    message['from'] = "udp-client"
else:
    message['from'] = args.title
message['payload'] = data
msg = json.dumps(message)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto(),
sock.sendto(bytes(msg+"\n", "utf-8"), (HOST, PORT))
#received = str(sock.recv(1024), "utf-8")

print("Sent: {}".format(data))
#print("Received: {}".format(received))