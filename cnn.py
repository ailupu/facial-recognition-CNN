import pickle
import numpy as np
import os
from tensorflow.keras import models
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization
from tensorflow.keras import regularizers

#path-ul catre directorul date unde au fost salvate datele pentru antrenare si testare
curent_dir = os.getcwd()
img_dir = os.path.join(curent_dir, "date")
os.chdir(img_dir)

# Citire fisiere cu date pentru imaginile cu lbp
with open('lbp_antrenare.txt', 'rb') as f:
    X_train = pickle.load(f)

with open('lbp_testare.txt', 'rb') as f:
    X_test = pickle.load(f)

with open('etichete_antrenare.txt', 'rb') as f:
    y_train = pickle.load(f)

with open('etichete_testare.txt', 'rb') as f:
    y_test = pickle.load(f)

# Citire fisiere cu date pentru imaginile simple
with open('crop_antrenare.txt', 'rb') as f:
    X_train_fata = pickle.load(f)

with open('crop_testare.txt', 'rb') as f:
    X_test_fata = pickle.load(f)

with open('crop_etichete_antrenare.txt', 'rb') as f:
    y_train_fata = pickle.load(f)

with open('crop_etichete_testare.txt', 'rb') as f:
    y_test_fata = pickle.load(f)

y_test = [[el] for el in y_test]
y_test = np.array(y_test)

y_train = [[el] for el in y_train]
y_train = np.array(y_train)

y_test_fata = [[el] for el in y_test_fata]
y_test_fata = np.array(y_test_fata)

y_train_fata = [[el] for el in y_train_fata]
y_train_fata = np.array(y_train_fata)

# Pregatire date de intrare
X_train = X_train.reshape(len(X_train), 154, 154, 1)
X_test = X_test.reshape(len(X_test), 154, 154, 1)

X_train_fata = X_train_fata.reshape(len(X_train_fata), 154, 154, 1)
X_test_fata = X_test_fata.reshape(len(X_test_fata), 154, 154, 1)

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

y_train_fata = to_categorical(y_train_fata)
y_test_fata = to_categorical(y_test_fata)

# Crearea modelului
model = models.Sequential()
# Optimizator = tf.keras.optimizers.Adam(learning_rate=0.000055)

model.add(Conv2D(16, kernel_size=(3, 3),
                 activation='relu',
                 kernel_regularizer=regularizers.l2(0.),
                 activity_regularizer=regularizers.l2(0.),
                 input_shape=(154, 154, 1)))

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(BatchNormalization())

model.add(Dropout(0.25))

model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 kernel_regularizer=regularizers.l2(0.),
                 activity_regularizer=regularizers.l2(0.)))

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(BatchNormalization())

model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(3000, activation='relu',
                kernel_regularizer=regularizers.l2(0.),
                activity_regularizer=regularizers.l2(0.)))

model.add(Dropout(0.25))

model.add(Dense(50, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Antrenare
#Testare pentru imaginile unde a fost calculat modelul local binar
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=27)

#Testare pentru imaginile unde sunt folosite doar fetele persoanelor
model.fit(X_train_fata, y_train_fata, validation_data=(X_test_fata, y_test_fata), epochs=27)

