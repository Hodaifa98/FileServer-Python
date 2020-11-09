#Import required modules.
import socket

def main():
    host = "127.0.0.1"
    port = 5000
    s = socket.socket()
    s.connect((host, port))
    file_name = input("File name: ")
    if file_name != "q":
        s.send(file_name.encode())
        data = s.recv(1024)
        if data[:6].decode() == "EXISTS":
            file_size = int(data[6:].decode())
            message = input(f"File exists: {file_size}Bytes. Download (Y/N)? ")
            if message == "Y" or message == "y":
                s.send("OK".encode())
                f = open(f"new_{file_name}", "wb")
                data = s.recv(1024)
                total_received = len(data)
                f.write(data)
                while total_received < file_size:
                    data = s.recv(1024)
                    total_received += len(data)
                    f.write(data)
                    print("{0:.2f}% done.".format((total_received/float(file_size)) * 100))
                print("Download is complete.")
        else:
            print("File doesn't exist.")
    s.close()

if __name__ == "__main__":
    main()