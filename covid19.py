# -*- coding: utf-8 -*-
"""covid19.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1L2kZfqPsdH3WUptE4DKjfxfv-O-oc_Lg
"""

# Dataset : http://cb.lk/covid_19

!wget http://cb.lk/covid_19

!unzip covid_19

TRAIN_PATH = "CovidDataset/Train"
VAL_PATH = "CovidDataset/Test"

import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.layers import *
from keras.models import *
from keras.preprocessing import image
from sklearn.metrics import precision_score, recall_score, f1_score
import os
from sklearn.metrics import confusion_matrix
import seaborn as sns

# CNN based model in keras

model = Sequential()
model.add(Conv2D(32,kernel_size=(3,3),activation='relu',input_shape=(224,224,3)))
model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(128,(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))


model.add(Flatten())
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1,activation='sigmoid'))

model.compile(loss=keras.losses.binary_crossentropy,optimizer='adam',metrics=['accuracy'])

model.summary()

#train

train_datagen = image.ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range = 0.2,
    horizontal_flip = True,
)

test_dataset = image.ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    'CovidDataset/Train',
    target_size = (224,224),
    batch_size=32,
    class_mode = 'binary'
)

train_generator.class_indices

validation_generator = test_dataset.flow_from_directory(
    'CovidDataset/Val',
    target_size = (224,224),
    batch_size=32,
    class_mode = 'binary'
)

hist = model.fit_generator(
    train_generator,
    steps_per_epoch=7,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=2
)

model.save("model_adv.h5")

model.evaluate(train_generator)

model.evaluate(validation_generator)

print(hist.history.keys())

plt.plot(hist.history['accuracy'])
plt.plot(hist.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

model = load_model("model_adv.h5")

train_generator.class_indices

y_actual = []
y_test = []

for i in os.listdir("./CovidDataset/Val/Normal/"):
    img = image.load_img("./CovidDataset/Val/Normal/"+i, target_size=(224,224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    p = model.predict_classes(img)
    y_test.append(p[0,0])
    y_actual.append(1)

for i in os.listdir("./CovidDataset/Val/Covid/"):
    img = image.load_img("./CovidDataset/Val/Covid/"+i, target_size=(224,224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    p = model.predict_classes(img)
    y_test.append(p[0,0])
    y_actual.append(0)

y_actual = np.array(y_actual)
y_test = np.array(y_test)

cm = confusion_matrix(y_actual, y_test)

sns.heatmap(cm, cmap="plasma", annot=True, xticklabels=['normal','covid'], yticklabels=['normal','covid'])

precision=precision_score(y_actual, y_test)
print('Precision: %.3f' % precision)

recall = recall_score(y_actual, y_test)
print('Recall: %.3f' % recall)

score = f1_score(y_actual, y_test)
print('F-Measure: %.3f' % score)