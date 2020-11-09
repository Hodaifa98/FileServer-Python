#Import required modules.
import os
import socket
import threading

def getFile(name: str, s):
    file_name = s.recv(1024)
    if os.path.isfile(file_name):
        size = str(os.path.getsize(file_name))
        msg = ("EXISTS" + size)
        s.send(msg.encode())
        user_response = s.recv(1024)
        if user_response[:2].decode() == "OK":
            with open(file_name, "rb") as f:
                bytes_to_send = f.read(1024)
                s.send(bytes_to_send)
                while bytes_to_send != "":
                    bytes_to_send = f.read(1024)
                    s.send(bytes_to_send)
    else:
        s.send("ERR".encode())
    s.close()

def main():
    host = "127.0.0.1"
    port = 5000
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print("Server started...")
    while True:
        con, address = s.accept()
        print(f"Client connected. IP: {str(address)}")
        t = threading.Thread(target=getFile, args=("getThread", con))
        t.start()
    s.close()

if __name__ == "__main__":
    main()