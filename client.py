import socket
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
if len(sys.argv) < 3:
    print(f"USAGE: python {sys.argv[0]} <SERVER ADDRESS> <SERVER PORT>")
    sys.exit(1)

# server address
serverAddr = sys.argv[1]

# server port
serverPort = int(sys.argv[2])

# create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
connSock.connect((serverAddr, serverPort))

# keep running
while True:
    # get the input from the user
    user_input = input("ftp> ")

    # if the command is get
    if user_input.startswith("get"):
        # send the entire input because we need to get data from the server
        connSock.send(user_input.encode())

        # the buffer to all data received from the the client
        fileData = ""

        # the temporary buffer to store the received data
        recvBuff = ""

        # the size of the incoming file
        fileSize = 0

        # the buffer containing the file size
        fileSizeBuff = ""

        # get the size of the buffer indicated by the first 10 bytes
        fileSizeBuff = recvAll(connSock, 10)

        try:
            # get the file size as an integer
            fileSize = int(fileSizeBuff)

            print(f"The file size is {fileSize} bytes.")

            # get the file data using the first 10 bytes
            fileData = recvAll(connSock, fileSize)

            print("The file content is:")
            print(fileData, "\n")
        except ValueError:
            print("Invalid file size format received from the server.")
        except FileNotFoundError:
            print("File doesn't exist!")

    # if the command is put
    elif user_input.startswith("put"):
        # the name of the file
        fileName = user_input[4:]
        try:
            # open the file
            with open(fileName, "r") as fileObj:
                # The number of bytes sent
                numSent = 0

                # the file data
                fileData = None

                # send the command so the server knows which command
                connSock.send("put".encode())

                # keep sending until all is sent
                while True:
                    # read the data
                    fileData = fileObj.read(65536)

                    # make sure we did not hit EOF
                    if fileData:
                        # get the size of the data
                        dataSizeStr = str(len(fileData))

                        # makes sure the dataSize is 10
                        while len(dataSizeStr) < 10:
                            dataSizeStr = "0" + dataSizeStr

                        # add the data size before the rest of the command
                        fileData = dataSizeStr + fileData

                        # the number of bytes sent
                        numSent = 0

                        # send the data
                        while len(fileData) > numSent:
                            numSent += connSock.send(fileData[numSent:].encode())

                    else:
                        break
                        # close the file because we're done

                print(f"Sent {numSent} bytes.\n")
        except FileNotFoundError:
            print("File doesn't exist!")

    # if the command is ls
    elif user_input.startswith("ls"):
        connSock.send("ls".encode())

        # get the first 10 which is the size of the ls command's return
        mySize = recvAll(connSock, 10)

        # print the command's output
        print(recvAll(connSock, int(mySize)), "\n")

    # exit the program
    elif user_input.startswith("quit"):
        print("Goodbye!")
        break

    else:
        print("Invalid command, try again!")

# close the socket
connSock.close()
