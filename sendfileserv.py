import socket
import subprocess
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


def handle_put_command(client_sock):
    """Handle 'put' command from the client"""
    # the buffer to all data received from the client
    file_data = ""

    # the size of the incoming file
    file_size = 0

    # the buffer containing the file size
    file_size_buff = ""

    # first 10 bytes indicate the file's size so we get that
    file_size_buff = recv_all(client_sock, 10)

    # convert the file size to an integer
    file_size = int(file_size_buff)

    print(f"The file size is {file_size} bytes.")

    # get the file data
    file_data = recv_all(client_sock, file_size)

    print("The file content is:")
    print(file_data)
    print("PUT COMMAND SUCCESSFUL\n")


def handle_ls_command(client_sock):
    """Handle 'ls' command from the client"""
    # run the command "ls" on the server and print the results on the server
    result = subprocess.getstatusoutput("ls")[1]

    # get the size of this output
    data_size = str(len(result))

    # make that output's size to 10 bytes
    while len(data_size) < 10:
        data_size = "0" + data_size

    # send it back to the client with the file size
    client_sock.send((data_size + result).encode())

    print("LS COMMAND SUCCESSFUL\n")


def handle_get_command(client_sock, data):
    """Handle 'get' command from the client"""
    # the name of the file
    filename = data[4:]

    try:
        # open the file
        with open(filename, "r") as file_obj:
            # the number of bytes sent
            num_sent = 0

            # the file data
            file_data = None

            # keep sending until all is sent
            while True:
                # read the data
                file_data = file_obj.read(65536)

                # make sure we did not hit EOF
                if file_data:
                    # get the size of the data read and convert it to string
                    data_size_str = str(len(file_data))

                    # prepend 0's to the size string until the size is 10 bytes
                    while len(data_size_str) < 10:
                        data_size_str = "0" + data_size_str

                    # prepend the size of the data to the file data
                    file_data = data_size_str + file_data

                    # the number of bytes sent
                    num_sent = 0

                    # send the data
                    while len(file_data) > num_sent:
                        num_sent += client_sock.send(file_data[num_sent:].encode())
                else:
                    break
                    # EOF so we're done

            print(f"Sent {num_sent} bytes.")
            print("GET COMMAND SUCCESSFUL\n")

    except FileNotFoundError:
        print("FAILED")
        print("FILE DOESN'T EXIST!")
        return True  # indicate failure


# command line checks
if len(sys.argv) != 2:
    print(f"USAGE: python {sys.argv[0]} <SERVER PORT>")
    sys.exit(1)

# the port on which to listen
listen_port = int(sys.argv[1])

# create a welcome socket
welcome_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the port
welcome_sock.bind(("", listen_port))

# start listening on the socket
welcome_sock.listen(1)

print("Waiting for connections...")

# accept connections
client_sock, addr = welcome_sock.accept()
print(f"Client: {addr} is connected!\n")

# accept connections forever
while True:
    # receive the data
    data = client_sock.recv(1024).decode()

    if data.startswith("put"):
        handle_put_command(client_sock)

    elif data.startswith("ls"):
        handle_ls_command(client_sock)

    elif data.startswith("get"):
        if handle_get_command(client_sock, data):
            break

    else:
        print(f"Client: {addr} disconnected!")
        break

# close the socket
client_sock.close()
