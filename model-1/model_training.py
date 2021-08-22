
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.applications import ResNet50

from load_training_data import get_training_data


def train_model():
    training_data, training_labels = get_training_data()

    print(training_data, training_labels)

    label_binarizer = LabelBinarizer()

    training_labels = label_binarizer.fit_transform(training_labels)
    training_labels = to_categorical(training_labels)

    base_model = ResNet50(pooling='avg', include_top=False,
                          input_shape=(224, 224, 3))

    head_model = base_model.output
    head_model = Flatten(name='flatten')(head_model)
    head_model = Dense(256, activation='relu')(head_model)
    head_model = Dropout(0.5)(head_model)
    head_model = Dense(2, activation='sigmoid')(head_model)

    model = Model(inputs=base_model.input, outputs=head_model)

    optimizer = Adam(lr=1e-4, decay=1e-4 / 20)

    epochs = 20

    model.compile(loss='binary_crossentropy',
                  optimizer=optimizer, metrics=['accuracy'])

    history = model.fit(training_data, training_labels,
                        epochs=epochs, validation_split=0.1, shuffle=True)

    model.save('clasificator')

    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0, epochs), history.history["loss"], label="train_loss")
    plt.plot(np.arange(0, epochs),
             history.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, epochs),
             history.history["accuracy"], label="train_acc")
    plt.plot(np.arange(0, epochs),
             history.history["val_accuracy"], label="val_acc")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig('grafic.png')
    plt.show()


train_model()
