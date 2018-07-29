import socket


def get_license(client):
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 60001  # Reserve a port for your service.

    s.connect((host, port))
    s.send("license" + client + ".info")
    s.recv(128)
    mLicense = open("license.info", "w")
    while True:
        l = s.recv(128)
        if l == '':
            break
        mLicense.write(l)
    print("Successfully Received file")
    s.close()
    print("connection closed")
    return


cID = raw_input("Enter Client ID: ")
get_license(cID)
