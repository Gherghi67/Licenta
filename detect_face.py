import cv2
import numpy as np


from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image

face_cascade = cv2.CascadeClassifier(
    './utils/haarcascade_frontalface_alt2.xml')

# Read the input image
img = cv2.imread('./test_images/eu_masca.jpg')


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.1, 4)

print(len(faces))

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    face = img[y:y + h, x:x + w]

    face = cv2.resize(face, (224, 224))

    cv2.imshow('poza', face)

    cv2.waitKey()

model = load_model('./Clasificatoare/Clasificator_Wild')

face_array = image.img_to_array(face)

face_batch = np.expand_dims(face_array, axis=0)

face_preprocessed = preprocess_input(face_batch)


predictions = model.predict(face_preprocessed)

if (np.argmax(predictions[0]) == 0):
    print('Cu masca')
else:
    print('Fara masca')
