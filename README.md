# CPSC 471 - Socket Programming Assignment
### Implementation of a simplified FTP server and FTP client.


## Collaborators:
* Alexis Vu (alexislayvu@csu.fullerton.edu)
* Christian Mendez (christianmendez@csu.fullerton.edu)
* Gilbert Espino Solis (Gil.espino18@gmail.com)

## Language used:
* Python

## How to run:
1) Execute `sendfileserv.py` in a Terminal window with the following command, replacing `<PORTNUMBER>` with your desired port number: `python sendfileserv.py <PORTNUMBER>`.
    - Example: `python sendfileserv.py 1234`
2) In a separate Terminal window, run `sendfilecli.py` using the following command, and again, replace `<PORTNUMBER>` with the same port number as before: `python sendfilecli.py localhost <PORTNUMBER>`.
    - Example: `python sendfilecli.py localhost 1234`
3) Upon connecting to the server, the client prints out `ftp>`, allowing you to execute the following commands:
    - `get <filename>`: Downloads file `<filename>` from the server.
        - Example: `ftp> get file.txt`
    - `put <filename>`: Uploads file `<filename>` to the server.
        - Example: `ftp> put file.txt`
    - `ls <filename>`: Lists files on the server.
        - Example: `ftp> ls file.txt`
    - `quit`: Disconnects from the server and exits the client.
        - Example: `ftp> quit`
4) Once you're finished, use the `quit` command to exit the program.
