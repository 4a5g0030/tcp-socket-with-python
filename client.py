import socket
import cv2
import pickle
import struct

host = ""
port = 12346

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

#cam config
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
img_counter = 1
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while 1:
    __, frame = cam.read()
    __, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)

    print("{}: {}".format(img_counter, size))
    client.sendall(struct.pack(">L", size) + data)
    img_counter += 1
    cv2.waitKey(5000)