import socket
import os
import sys


# used to receive the data by providing the number of bytes to receive
def recvAll(sock, numBytes):
    # The buffer
    recvBuff = ""

    # The temporary buffer
    tmpBuff = ""

    # Keep receiving until all is received
    while len(recvBuff) < numBytes:
        # Attempt to receive bytes
        tmpBuff = sock.recv(numBytes)

        # The other side has closed the socket
        if not tmpBuff:
            break

        # Add the received bytes to the buffer
        recvBuff += tmpBuff.decode()

    return recvBuff


# Command line checks
if len(sys.argv) < 3:
    print("USAGE python " + sys.argv[0] + " <SERVER ADDRESS> <SERVER PORT>")
    sys.exit(1)

# Server address
serverAddr = sys.argv[1]

# Server port
serverPort = int(sys.argv[2])

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

# keep running
while True:
    # get the input from the user
    response = input("ftp> ")
    
    if len(response) < 5:
        command = response
    else:
        command, fileName = response.split()

    # check if the command is put
    if command == "put":
        # The name of the file
        try:
            # Open the file
            with open(fileName, "r") as fileObj:
                # The number of bytes sent
                numSent = 0

                # The file data
                fileData = None

                # send the command so the server knows which command
                connSock.send("put".encode())

                # Keep sending until all is sent
                while True:
                    # Read the data
                    fileData = fileObj.read(65536)

                    # Make sure we did not hit EOF
                    if fileData:
                        # get the size of the data
                        dataSizeStr = str(len(fileData))

                        # makes sure the dataSize is 10
                        while len(dataSizeStr) < 10:
                            dataSizeStr = "0" + dataSizeStr

                        # add the data size before the rest of the command
                        fileData = dataSizeStr + fileData

                        # The number of bytes sent
                        numSent = 0

                        # Send the data!
                        while len(fileData) > numSent:
                            numSent += connSock.send(fileData[numSent:].encode())

                    else:
                        break
                        # close the file because we're done

                print("Sent", numSent, "bytes.\n")
        except FileNotFoundError:
            print("File doesn't exist!")

    # command was to get
    elif command == "get":
        if os.path.exists(fileName):
        
            # send the entire input because we need to get data from the server
            connSock.send(response.encode())

            # The buffer to all data received from the
            # the client.
            fileData = ""

            # The temporary buffer to store the received
            # data.
            recvBuff = ""

            # The size of the incoming file
            fileSize = 0

            # The buffer containing the file size
            fileSizeBuff = ""

            # get the size of the buffer indicated by the first 10 bytes
            fileSizeBuff = recvAll(connSock, 10)

            # Get the file size as an integer
            fileSize = int(fileSizeBuff)

            print("The file size is", fileSize, "bytes.")

            # Get the file data using the first 10 bytes
            fileData = recvAll(connSock, fileSize)

            print("The file content is:")
            print(fileData, "\n")
        else:
            print(f"File {fileName} does not exist!")

    # send the ls command to the server
    elif command == "ls":
        connSock.send("ls".encode())

        # get the first 10 which is the size of the ls command's return
        mySize = recvAll(connSock, 10)
        # print the command's output
        print(recvAll(connSock, int(mySize)), '\n')
        

    # exit the program
    elif command == "quit":
        print("Goodbye!")
        break
        

# close the socket
connSock.close()
