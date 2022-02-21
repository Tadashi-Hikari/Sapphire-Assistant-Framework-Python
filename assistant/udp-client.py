# This just takes stdin an sends it as a UDP over the proper port.
import socket, sys, json, argparse

def mute():
    sys.stderr = None
    sys.stdout = None

if __name__ == '__main__':
    HOST, PORT = "localhost", 9999

    # read stdin, as opposed to the command-line options
    #data = sys.stdin.read()
    title = "udp-client.py"
    data = ""

    #if(data.startswith("-")):
    parser = argparse.ArgumentParser(description="datagram messenger to sapphire framework assistant")
    parser.add_argument('-t', dest='title', help="set a title for the origin of this datagram",nargs='*')
    try:
        mute()
        args = parser.parse_args()
        title = args.title[0]
        data = " ".join(sys.argv[3:])
    except BaseException:
        data = " ".join(sys.argv[1:])

    # SOCK_DGRAM is the socket type to use for UDP sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = {}
    message['from'] = title
    message['payload'] = data
    msg = json.dumps(message)

    # As you can see, there is no connect() call; UDP has no connections.
    # Instead, data is directly sent to the recipient via sendto(),
    sock.sendto(bytes(msg+"\n", "utf-8"), (HOST, PORT))

    print("Sent: {}".format(data))