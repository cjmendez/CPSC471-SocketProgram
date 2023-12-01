import socket
import sys


def recv_all(sock, num_bytes):
    """Function to receive all data from a socket"""

    # the buffer
    recv_buff = ""

    # the temporary buffer
    tmp_buff = ""

    # keep receiving until all is received
    while len(recv_buff) < num_bytes:
        # attempt to receive bytes
        tmp_buff = sock.recv(num_bytes)

        # the other side has closed the socket
        if not tmp_buff:
            break
        # add the received bytes to the buffer
        recv_buff += tmp_buff.decode()

    return recv_buff


# command line checks
if len(sys.argv) < 3:
    print(f"USAGE: python {sys.argv[0]} <SERVER ADDRESS> <SERVER PORT>")
    sys.exit(1)

# server address
server_addr = sys.argv[1]

# server port
server_port = int(sys.argv[2])

# create a TCP socket
conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
conn_sock.connect((server_addr, server_port))

# keep running
while True:
    # get user input
    user_input = input("ftp> ")

    if user_input.startswith("put"):
        # the name of the file
        filename = user_input[4:]

        try:
            # open the file
            with open(filename, "r") as file_obj:
                # the number of bytes sent
                num_sent = 0

                # the file data
                file_data = None

                # send the command so the server knows which command
                conn_sock.send("put".encode())

                # keep sending until all is sent
                while True:
                    # read the data
                    file_data = file_obj.read(65536)

                    # make sure we did not hit EOF
                    if file_data:
                        # get the size of the data
                        data_size_str = str(len(file_data))

                        # makes sure the dataSize is 10
                        while len(data_size_str) < 10:
                            data_size_str = "0" + data_size_str

                        # add the data size before the rest of the command
                        file_data = data_size_str + file_data

                        # the number of bytes sent
                        num_sent = 0

                        # send the data
                        while len(file_data) > num_sent:
                            num_sent += conn_sock.send(file_data[num_sent:].encode())

                    else:
                        break
                        # close the file because we're done

                print(f"Sent {num_sent} bytes.\n")

        except FileNotFoundError:
            print("File doesn't exist!")

    elif user_input.startswith("get"):
        # send the entire input because we need to get data from the server
        conn_sock.send(user_input.encode())

        # the buffer to all data received from the the client
        file_data = ""

        # the temporary buffer to store the received data
        recv_buff = ""

        # The size of the incoming file
        file_size = 0

        # The buffer containing the file size
        file_size_buff = ""

        # get the size of the buffer indicated by the first 10 bytes
        file_size_buff = recv_all(conn_sock, 10)

        # get the file size as an integer
        file_size = int(file_size_buff)

        print(f"The file size is {file_size} bytes.")

        # get the file data using the first 10 bytes
        file_data = recv_all(conn_sock, file_size)

        print("The file content is:")
        print(file_data, "\n")

    elif user_input.startswith("ls"):
        conn_sock.send("ls".encode())

        # get the first 10 which is the size of the ls command's return
        mySize = recv_all(conn_sock, 10)

        # print the command's output
        print(recv_all(conn_sock, int(mySize)), "\n")

    elif user_input.startswith("quit"):
        print("Goodbye!")
        break

    else:
        print("Unknown command, try again.")

# close the socket
conn_sock.close()
