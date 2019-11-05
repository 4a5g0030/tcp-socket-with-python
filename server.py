import socket
import cv2
import pickle
import struct

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

bin_ip = socket.gethostbyname(socket.gethostname())
bin_port = 12345

server.bind((bin_ip, bin_port))
server.listen(1)

print("Listing on %s:%d" % (bin_ip, bin_port))

while 1:
    client, address = server.accept()
    print("Connect by : ", address)

    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))

    while 1:
        while len(data) < payload_size:
            print("Recv: {}".format(len(data)))
            data += client.recv(4096)

        print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))
        while len(data) < msg_size:
            data += client.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow('ImageWindow', frame)
        cv2.waitKey(1)