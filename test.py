# -*- coding: UTF-8 -*-
from keras.datasets import mnist
from keras.utils import np_utils
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from keras.models import Model
import os
# import Image
import numpy as np
from keras.models import Sequential
from keras.layers import  Dense,Dropout,Flatten,Conv2D,MaxPool2D

train0=np.load('X_data0.npy') #(614, 280, 280, 3)
train1=np.load('X_data1.npy') #(318, 280, 280, 3)
X_Train=np.vstack((train0, train1))
print(np.shape(X_Train))

Y_Train = np.zeros((932))
for i in range(0,614,1):
    Y_Train[i] = 0
for i in range(614,932,1):
    Y_Train[i] = 1


#
# test0=np.load('Y_data0.npy') #(8, 280, 280, 3)
# test1=np.load('Y_data1.npy') #(8, 280, 280, 3)
# X_test=np.vstack((test0, test1))
#
# Y_test = np.zeros((16))
# for i in range(0,8,1):
#     Y_Train[i] = 0
# for i in range(8,16,1):
#     Y_Train[i] = 1

# Translation of data
X_Train = X_Train.astype('float32')

# Label Onehot-encoding
Y_Train = np_utils.to_categorical(Y_Train)

print (Y_Train[:])

# Standardize feature data
X_Train /= 255
# X_test /= 255
# print(Y_Train)

model = Sequential()

# Create CN layer 1
model.add(Conv2D(filters=16,
                 kernel_size=(5,5),
                 padding='same',
                 input_shape=(280,280,3),
                 activation='relu'))

# Create Max-Pool 1
model.add(MaxPool2D(pool_size=(2,2)))

# Create CN layer 2
model.add(Conv2D(filters=36,
                 kernel_size=(5,5),
                 padding='same',
                 input_shape=(280,280,3),
                 activation='relu'))

# Create Max-Pool 2
model.add(MaxPool2D(pool_size=(2,2)))

# Add Dropout layer
model.add(Dropout(0.25))

# Create Flat layer
model.add(Flatten())

# Create Hidden layer
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))

# Add Dropout layer
model.add(Dense(2, activation='softmax'))

# See the model's summary
model.summary()

# Define training methods
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


# print(X_Train[0])
# Strat training
train_history = model.fit(x = X_Train,
                          y = Y_Train,
                          validation_split=0.1,
                          epochs=10,
                          batch_size=1,
                          verbose=2)

score = model.evaluate(X_Train, Y_Train, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# preds = model.predict(X_test)
#
# for i in range(0,15,1):
#     if preds[i][0] > preds[i][1]:
#         print ("院長")
#     else:
#         print("其他")