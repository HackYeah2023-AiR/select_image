# Tiny Yolo 3 model test program
# BlackMagicai.com
import numpy as np
import time
from keras.models import load_model
from PIL import Image, ImageDraw
import os
from yolofn import yolo_out, draw
from io import BytesIO


FOLDER_NAME = "Tiny-Yolo-3/example"
SIZE = (416, 416)


def get_box(input_image_name):
    yolo = load_model("yolotest.h5py")
    image_src = Image.open(BytesIO(input_image_name))
    image_thumb = image_src.resize(SIZE, Image.BICUBIC)

    image = np.array(image_thumb, dtype="float32")
    image /= 255.0
    image = np.expand_dims(image, axis=0)

    start = time.time()
    output = yolo.predict(image)
    end = time.time()

    print("Processing time: {0:.2f}s".format(end - start))

    with open("coco_classes.txt") as f:
        class_names = f.readlines()
    all_classes = [c.strip() for c in class_names]

    thumb_size = image_thumb.size
    boxes, classes, scores = yolo_out(output, thumb_size)
    box = None
    if boxes is not None:
        draw(image_thumb, boxes, scores, classes, all_classes)
        box = boxes[0]
    image_thumb.save(f"out/{input_image_name}", "JPEG")
    return box


def select_image(box, input_image_name):
    box = get_box(input_image_name)
    file_name, _ = os.path.splitext(input_image_name)
    output_image_path = f"out/{file_name}_frame.jpg"
    image = Image.open(f"out/{input_image_name}")

    x, y, w, h = box
    offset = 2
    top = max(0, y + 0.5) + offset
    left = max(0, x + 0.5) + offset
    right = min(image.size[0], x + w + 0.5) - offset
    bottom = min(image.size[1], y + h + 0.5) - offset

    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save(output_image_path, "JPEG")


# if __name__ == "__main__":
#     input_image_name = "dogy.jpg"
#     select_image(input_image_name)
