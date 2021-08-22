import os
import numpy as np


from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.resnet50 import preprocess_input

labels = []


def loop_folders(path, label):
    data = []

    directory = path

    for image_name in os.listdir(directory):
        image_path = os.path.join(directory, image_name)

        if (image_path.endswith('.jpg')):

            image = load_img(image_path, target_size=(224, 224))
            image = img_to_array(image)
            image = preprocess_input(image)

            data.append(image)
            labels.append(label)

    return data


def get_training_data():

    data = loop_folders(
        '../Dataset/training_data/with_mask/00000', 0)
    data.extend(loop_folders(
        '../Dataset/training_data/without_mask/00000', 1))

    data = np.array(data)
    array_labels = np.array(labels)

    return data, array_labels
