import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

bin_ip = socket.gethostbyname(socket.gethostname())
bin_port = 12345

server.bind((bin_ip, bin_port))
server.listen(1)

print("Listing on %s:%d" % (bin_ip, bin_port))

while 1:
    client, address = server.accept()
    print("Connect by : ", address)

    while 1 :
        msg = client.recv(1024)
        print("msg : " + str(msg))
        rt_msg = "OK!"
        client.send(rt_msg.encode("utf-8"))