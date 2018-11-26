from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras import backend as K

from keras.utils import np_utils

import time

class bl_cifar10():

    def __init__(self):
        (x_train, y_train), (x_test, y_test) = cifar10.load_data()

        self.x_train = x_train / 255
        self.x_test = x_test / 255

        self.y_train = np_utils.to_categorical(y_train)
        self.y_test = np_utils.to_categorical(y_test)
        
        self.num_classes = self.y_test.shape[1]


    def gen_model(self, x, y):

        model = Sequential()
        model.add(Conv2D(8,  kernel_size=(3,3), activation='relu', input_shape=x.shape))
        model.add(Conv2D(16, kernel_size=(3,3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.2))
        model.add(Conv2D(16, kernel_size=(3,3), activation='relu'))
        model.add(Conv2D(8,  kernel_size=(3,3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(y, activation='softmax'))
        return model
        
    def run_bl(self):
        start_time = time.time()

        model = self.gen_model(self.x_train[0], self.num_classes)
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        data = model.fit(self.x_train, self.y_train, validation_data=(self.x_test, self.y_test), epochs=50, batch_size=200, verbose=2)

        score = model.evaluate(self.x_test, self.y_test, verbose=0)

        elapsed_time = time.time() - start_time
        return elapsed_time


