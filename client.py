import socket

host = "192.168.1.12"
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

while True:
    msg = input("Please input msg:")
    client.send(msg.encode("utf-8"))
    data = client.recv(1024)
    print("Server return :" + str(data))