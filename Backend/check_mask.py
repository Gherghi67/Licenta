import cv2
import numpy as np

from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image


async def check_mask(model, file):
    face_cascade = cv2.CascadeClassifier(
        '../utils/haarcascade_frontalface_alt2.xml')

    file_image = await file.read()

    np_img = np.fromstring(file_image, np.uint8)

    img = cv2.imdecode(np_img, cv2.cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        face = img[y:y + h, x:x + w]

        face = cv2.resize(face, (224, 224))

    face_array = image.img_to_array(face)

    face_batch = np.expand_dims(face_array, axis=0)

    face_preprocessed = preprocess_input(face_batch)

    predictions = model.predict(face_preprocessed)

    if (np.argmax(predictions[0]) == 0):
        return True

    return False
