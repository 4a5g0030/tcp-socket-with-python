import cv2


cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320);
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 240);

while 1:
    __, frame = cam.read()
    cv2.imshow('window', frame)
    cv2.waitKey(1)