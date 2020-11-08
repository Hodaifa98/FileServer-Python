#Import required modules.
import os
import socket
import threading

def getFile(name: str, s: socket):
    file_name = s.recv(1024)
    if os.path.isfile(file_name):
        size = str(os.path.getsize(file_name))
        s.send(f"EXISTS {size}")
        user_response = s.recv(1024)
        if user_response[::2] == "OK":
            with open(file_name, "rb") as f:
                bytes_to_send = f.read(1024)
                s.send(bytes_to_send)
                while bytes_to_send != "":
                    bytes_to_send = f.read(1024)
                    s.send(bytes_to_send)
    else:
        s.send("ERR")
    s.close()