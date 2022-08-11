from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import os

from imutils import paths
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report
import pickle
import matplotlib.pyplot as plt


class BuilderThread(QThread):
    def __init__(self, compileTrainSaveWidget, trainingParamsWidget, dataAugmentationParamsWidget):
        super().__init__()
        os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
        self.datasetPath = compileTrainSaveWidget.datasetPath
        self.modelPath = compileTrainSaveWidget.modelPath
        self.encoderPath = compileTrainSaveWidget.encoderPath
        self.plotPath = compileTrainSaveWidget.plotPath
        self.initLearnRate = trainingParamsWidget.learningRate.value()
        self.epochs = int(trainingParamsWidget.epochs.value())
        self.batchSize = int(trainingParamsWidget.batchSize.value())
        self.testTrainSplit = trainingParamsWidget.testTrainSplit.value()
        self.imDim = int(trainingParamsWidget.imagesDims.value())
        self.rotationRange = int(dataAugmentationParamsWidget.rotationRange.value())
        self.zoomRange = dataAugmentationParamsWidget.zoomRange.value()
        self.widthShiftRange = dataAugmentationParamsWidget.widthShiftRange.value()
        self.heightShiftRange = dataAugmentationParamsWidget.heightShiftRange.value()
        self.shearRange = dataAugmentationParamsWidget.shearRange.value()
        self.hFlip = True if dataAugmentationParamsWidget.horizontalFlip.isChecked() is True else False
        self.vFlip = True if dataAugmentationParamsWidget.verticalFlip.isChecked() is True else False
        self.fillMode = dataAugmentationParamsWidget.fillMode.currentText()

        self.threadActive = False
    
    def stop(self):
        self.threadActive = False

    def play(self):
        self.threadActive = True

    def run(self):
        print("[INFO] loading images... (this may take several minutes)")
        imagePaths = list(paths.list_images(self.datasetPath))
        data = []
        labels = []
        uniquelabels = []

        # loop over the image paths
        for imagePath in imagePaths:
            # extract the class label from the filename
            label = imagePath.split(os.path.sep)[-2]
            # load the input image and preprocess it
            image = load_img(imagePath, target_size=(self.imDim, self.imDim))
            image = img_to_array(image)
            image = preprocess_input(image)

            # update the data and labels lists, respectively
            data.append(image)
            labels.append(label)

            newlabel = True
            for i in range(len(uniquelabels)):
                if uniquelabels[i] == label:
                    newlabel = False
            if newlabel is True:
                uniquelabels.append(label)
        print("[INFO] unique labels found: ", uniquelabels)

        # convert the data and labels to NumPy arrays
        data = np.array(data, dtype="float32")
        # data = np.array(data, dtype="uint8")
        labels = np.array(labels)

        # perform one-hot encoding on the labels
        lb = LabelEncoder()
        labels = lb.fit_transform(labels)
        labels = to_categorical(labels)

        # partition the data into training and testing splits using 75% of
        # the data for training and the remaining 25% for testing
        (trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=self.testTrainSplit, stratify=labels, random_state=42)

        # construct the training image generator for data augmentation
        aug = ImageDataGenerator(
            rotation_range=self.rotationRange,
            zoom_range=self.zoomRange,
            width_shift_range=self.widthShiftRange,
            height_shift_range=self.heightShiftRange,
            shear_range=self.shearRange,
            horizontal_flip=self.hFlip,
            vertical_flip=self.vFlip,
            fill_mode=self.fillMode
        )

        # load the MobileNetV2 network, ensuring the head FC layer sets are
        # left off
        baseModel = MobileNetV2(
            input_shape=(self.imDim, self.imDim, 3),
            weights="imagenet",
            include_top=False,
            input_tensor=Input(shape=(self.imDim, self.imDim, 3))
        )

        # construct the head of the model that will be placed on top of the
        # the base model
        headModel = baseModel.output
        headModel = AveragePooling2D(pool_size=(7, 7), padding='same')(headModel)
        headModel = Flatten(name="flatten")(headModel)
        headModel = Dense(128, activation="relu")(headModel)
        headModel = Dropout(0.5)(headModel)
        headModel = Dense(len(uniquelabels), activation="softmax")(headModel)

        # place the head FC model on top of the base model (this will become
        # the actual model we will train)
        model = Model(inputs=baseModel.input, outputs=headModel)

        # loop over all layers in the base model and freeze them so they will
        # *not* be updated during the first training process
        for layer in baseModel.layers:
            layer.trainable = False

        # compile our model
        print("[INFO] compiling model...")
        opt = Adam(learning_rate=self.initLearnRate)
        model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

        # train the head of the network
        print("[INFO] training head...")
        H = model.fit(
            aug.flow(trainX, trainY, batch_size=self.batchSize),
            # steps_per_epoch=len(trainX) // BS,
            validation_data=(testX, testY),
            # validation_steps=len(testX) // BS,
            epochs=self.epochs
        )

        # make predictions on the testing set
        print("[INFO] evaluating network...")
        predIdxs = model.predict(testX, batch_size=self.batchSize)

        # for each image in the testing set we need to find the index of the
        # label with corresponding largest predicted probability
        predIdxs = np.argmax(predIdxs, axis=1)

        # show a nicely formatted classification report
        print(classification_report(testY.argmax(axis=1), predIdxs, target_names=lb.classes_))

        # serialize the model to disk
        print("[INFO] saving mask detector model...")
        model.save(self.modelPath, save_format="h5")

        # serialize the label encoder to disk
        print("[INFO] saving label encoder...")
        f = open(self.encoderPath, "wb")
        f.write(pickle.dumps(lb))
        f.close()

        # plot the training loss and accuracy
        print("[INFO] saving plot...")
        N = self.epochs
        plt.style.use("ggplot")
        plt.figure()
        plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
        plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
        plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
        plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
        plt.title("Training Loss and Accuracy")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend(loc="lower left")
        plt.savefig(self.plotPath)

        print("[INFO] Completed!")
        