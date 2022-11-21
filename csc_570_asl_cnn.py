# -*- coding: utf-8 -*-
"""CSC 570 ASL CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DdAC_XDHGTV0DwizYJ9ucPtOSUWj5jOQ
"""

!wget https://github.com/Hadiasemi/American-Sign-Language-Translator-Web-Application/blob/main/data/sign_mnist_test/sign_mnist_test.csv

!git clone https://arafian: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@github.com/Hadiasemi/American-Sign-Language-Translator-Web-Application.git

!ls

# Commented out IPython magic to ensure Python compatibility.
!git clone https://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@github.com/Hadiasemi/American-Sign-Language-Translator-Web-Application.git

# %cd American-Sign-Language-Translator-Web-Application/data/

import pandas as pd

train_df = pd.read_csv("sign_mnist_train.csv")
test_df = pd.read_csv("sign_mnist_test.csv")

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def show_image(image):
  try:
    plt.imshow(image.reshape(28, 28) , cmap = "gray")
  except:    
    plt.imshow(image, cmap = "gray")

# show_image(test[10].reshape(28, 28))

# Training sets
X_train = np.array(train_df.drop("label", axis=1)) / 255
y_train = train_df['label']

# Test sets
X_test = np.array(test_df.drop("label", axis=1)) / 255
y_test = test_df['label']

# Reshaping for CNN
X_train = X_train.reshape(-1,28,28,1)
X_test = X_test.reshape(-1,28,28,1)

from sklearn.preprocessing import LabelBinarizer
label_binarizer = LabelBinarizer()
y_train = label_binarizer.fit_transform(y_train)
y_test = label_binarizer.fit_transform(y_test)

import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D , MaxPool2D , Flatten , Dropout , BatchNormalization

model = Sequential()
model.add(Conv2D(75 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu' , input_shape = (28,28,1)))
# model.add(BatchNormalization())
# model.add(MaxPool2D((2,2) , strides = 2 , padding = 'same'))
# model.add(Conv2D(50 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu'))
# model.add(Dropout(0.2))
# model.add(BatchNormalization())
# model.add(MaxPool2D((2,2) , strides = 2 , padding = 'same'))
# model.add(Conv2D(25 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu'))
# model.add(BatchNormalization())
# model.add(MaxPool2D((2,2) , strides = 2 , padding = 'same'))
model.add(Flatten())
# model.add(Dense(units = 512 , activation = 'relu'))
# model.add(Dropout(0.3))
model.add(Dense(units = 24 , activation = 'softmax'))
model.compile(optimizer = 'adam' , loss = 'categorical_crossentropy' , metrics = ['accuracy'])
model.summary()

# commented out is the OG fit call, look at it for hyperparameters
# history = model.fit(datagen.flow(x_train,y_train, batch_size = 128) ,epochs = 20 , validation_data = (x_test, y_test) , callbacks = [learning_rate_reduction])


history = model.fit(X_train, y_train, epochs = 10, validation_data = (X_test, y_test))

preds = model.predict(X_test)

np.argmax(preds[0])

preds[0]

