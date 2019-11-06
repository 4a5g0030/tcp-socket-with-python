import socket
import cv2
import pickle
import struct
import os
import mrcnn.model as modellib
from mrcnn.config import Config
import numpy as np

ROOT_DIR = os.getcwd()
MODEL_DIR = os.path.join(ROOT_DIR, 'logs')
MODEL_WEIGHT_PATH = os.path.join(MODEL_DIR, 'mask_rcnn_animal_0018.h5')


def random_colors(N):
    np.random.seed(1)
    colors = [tuple(255 * np.random.rand(3)) for _ in range(N)]
    return colors


def apply_mask(image, mask, color, alpha=0.5):
    """apply mask to image"""
    for n, c in enumerate(color):
        image[:, :, n] = np.where(
            mask == 1,
            image[:, :, n] * (1 - alpha) + alpha * c,
            image[:, :, n]
        )
    return image


def display_instances(image, boxes, masks, ids, names, scores):
    """
        take the image and results and apply the mask, box, and Label
    """
    n_instances = boxes.shape[0]
    colors = random_colors(n_instances)

    if not n_instances:
        print('NO INSTANCES TO DISPLAY')
    else:
        assert boxes.shape[0] == masks.shape[-1] == ids.shape[0]

    for i, color in enumerate(colors):
        if not np.any(boxes[i]):
            continue

        y1, x1, y2, x2 = boxes[i]
        label = names[ids[i]]
        score = scores[i] if scores is not None else None
        caption = '{} {:.2f}'.format(label, score) if score else label
        mask = masks[:, :, i]

        image = apply_mask(image, mask, color)
        image = cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        image = cv2.putText(
            image, caption, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.7, color, 2
        )

    return image


class BottleConfig(Config):
    NAME = "animal"

    IMAGES_PER_GPU = 2

    NUM_CLASSES = 1 + 2


class InferenceConfig(BottleConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


config = InferenceConfig()
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
model.load_weights(MODEL_WEIGHT_PATH, by_name=True)
class_names = ['BG', 'dog', 'cat']

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

bin_ip = socket.gethostbyname(socket.gethostname())
bin_port = 12346

server.bind((bin_ip, bin_port))
server.listen(1)

print("Listing on %s:%d" % (bin_ip, bin_port))

while 1:
    client, address = server.accept()
    print("Connect by : ", address)

    data = b""
    payload_size = struct.calcsize(">L")
    # print("payload_size: {}".format(payload_size))

    while 1:
        while len(data) < payload_size:
            # print("Recv: {}".format(len(data)))
            data += client.recv(4096)

        # print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        # print("msg_size: {}".format(msg_size))

        while len(data) < msg_size:
            data += client.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        results = model.detect([frame], 0)
        r = results[0]
        frame = display_instances(frame, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])

        cv2.imshow('frame', frame)
        cv2.waitKey(1)

        for item in r['class_ids']:
            print(class_names[item])
