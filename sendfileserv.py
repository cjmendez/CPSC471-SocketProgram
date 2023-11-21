import socket
import subprocess
import sys

# the port on which to listen
serverPort = int(sys.argv[1])

# create a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the port
serverSocket.bind(("", serverPort))

# start listening for incoming connections
serverSocket.listen(1)

# print("The server is ready to receive.")


# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):
    # the buffer
    recvBuff = ""

    # the temporary buffer
    tmpBuff = ""

    # keep receiving till all is received
    while len(recvBuff) < numBytes:
        # attempt to receive bytes
        tmpBuff = sock.recv(numBytes)

        # the other side has closed the socket
        if not tmpBuff:
            break

        # add the received bytes to the buffer
        recvBuff += tmpBuff

    return recvBuff
