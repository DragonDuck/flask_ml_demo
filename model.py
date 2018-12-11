import keras
import keras.models as kmod
import keras.layers as klay
import keras.utils as kutils
import os
from PIL import Image
import numpy as np


def classify_image(fname):
    """
    Classify an image using a pretrained model
    :param fname: Path to image
    :return:
    """
    model = load_model()
    image = np.array(Image.open(fname))[np.newaxis, ..., np.newaxis]
    return model.predict(image).argmax()


def train_classifier(outfile):
    """
    Train a DNN classifier on MNIST data and persist the model.

    There is currently no provision to run this within the Flask framework.
    :param outfile: Path to persist model to
    :return:
    """

    # Load data
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # Transform labels
    y_train_cat = kutils.to_categorical(y_train)
    y_test_cat = kutils.to_categorical(y_test)

    # Transform input to be 4D
    x_train = x_train[..., None]
    x_test = x_test[..., None]

    # create model
    model = kmod.Sequential()

    # add model layers
    model.add(klay.Conv2D(
        filters=32, kernel_size=3, activation='relu',
        input_shape=x_train.shape[1:]))
    model.add(klay.MaxPool2D())
    model.add(klay.Conv2D(
        filters=32, kernel_size=3, activation='relu',
        kernel_initializer="glorot_uniform"))
    model.add(klay.MaxPool2D())
    model.add(klay.Conv2D(
        filters=32, kernel_size=3, activation='relu',
        kernel_initializer="glorot_uniform"))
    model.add(klay.Flatten())
    model.add(klay.Dense(
        units=10, activation='softmax',
        kernel_initializer="glorot_uniform"))

    # compile model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train_cat, validation_data=(x_test, y_test_cat), epochs=5)
    model.save(outfile)

    return None


def load_model():
    """
    Interface function to load a trained model from disk
    :return:
    """
    return keras.models.load_model(os.path.join("static", "model.keras"))
