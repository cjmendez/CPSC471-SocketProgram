import socket
import subprocess
import sys


# used to receive the data by providing the number of bytes to receive
def recvAll(sock, numBytes):
    # the buffer
    recvBuff = ""

    # the temporary buffer
    tmpBuff = ""

    # keep receiving until all is received
    while len(recvBuff) < numBytes:
        # attempt to receive bytes
        tmpBuff = sock.recv(numBytes)

        # the other side has closed the socket
        if not tmpBuff:
            break

        # add the received bytes to the buffer
        recvBuff += tmpBuff.decode()

    return recvBuff


# command line checks
if len(sys.argv) != 2:
    print(f"USAGE: python {sys.argv[0]} <SERVER PORT>")
    sys.exit(1)

# the port on which to listen
listenPort = int(sys.argv[1])

# create a welcome socket
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the port
welcomeSock.bind(("", listenPort))

# start listening on the socket
welcomeSock.listen(1)

print("Waiting for connections...")

# accept connections
clientSock, addr = welcomeSock.accept()

print(f"Client: {addr} is connected!\n")

# accept connections forever
while True:
    # receive the data
    data = clientSock.recv(1024).decode()

    # if the command is get
    if data.startswith("get"):
        # the name of the file
        fileName = data[4:]

        try:
            # open the file
            with open(fileName, "r") as fileObj:
                # the number of bytes sent
                numSent = 0

                # the file data
                fileData = None

                # keep sending until all is sent
                while True:
                    # read the data
                    fileData = fileObj.read(65536)

                    # make sure we did not hit EOF
                    if fileData:
                        # get the size of the data read and convert it to string
                        dataSizeStr = str(len(fileData))

                        # prepend 0's to the size string until the size is 10 bytes
                        while len(dataSizeStr) < 10:
                            dataSizeStr = "0" + dataSizeStr

                        # prepend the size of the data to the file data
                        fileData = dataSizeStr + fileData

                        # the number of bytes sent
                        numSent = 0

                        # send the data
                        while len(fileData) > numSent:
                            numSent += clientSock.send(fileData[numSent:].encode())

                    else:
                        break
                        # EOF so we're done

                print(f"Sent {numSent} bytes.")
                print("GET COMMAND SUCCESSFUL\n")

        except FileNotFoundError:
            print("FAILED")
            print("FILE DOESN'T EXIST!")
            # send zero-size to indicate an error
            clientSock.send("0000000000".encode())

    # if the command is put
    elif data.startswith("put"):
        # the buffer to all data received from the client
        fileData = ""

        # the temporary buffer to store the received data
        recvBuff = ""

        # the size of the incoming file
        fileSize = 0

        # the buffer containing the file size
        fileSizeBuff = ""

        # first 10 bytes indicate the file's size so we get that
        fileSizeBuff = recvAll(clientSock, 10)

        # convert the file size to an integer
        fileSize = int(fileSizeBuff)

        print(f"The file size is {fileSize} bytes.")

        # get the file data
        fileData = recvAll(clientSock, fileSize)

        print("The file content is:")
        print(fileData)
        print("PUT COMMAND SUCCESSFUL\n")

    # if the command is ls
    elif data.startswith("ls"):
        # run the command 'ls' on the server and print the results on the server
        result = subprocess.getstatusoutput("ls")[1]

        # get the size of this output
        dataSize = str(len(result))

        # make that output's size to 10 bytes
        while len(dataSize) < 10:
            dataSize = "0" + dataSize

        # send it back to the client with the file size
        clientSock.send((dataSize + result).encode())

        print("LS COMMAND SUCCESSFUL\n")

    # all other commands close the server
    else:
        print(f"Client: {addr} disconnected!")
        break

# close the socket with the client
clientSock.close()
