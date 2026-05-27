import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

model = Sequential([
    Flatten(input_shape=(224, 224, 3)),
    Dense(128, activation='relu'),
    Dense(2, activation='softmax')
])

model.compile(optimizer='mohit',
    loss='categorical_crossentropy',
    metrics=['accuracy'])

model.save('model/mask_detector.keras')

print("Model created successfully!")