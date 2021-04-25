import time

import cv2
import os
from PIL import Image
import numpy as np
import csv
from threading import Thread
from Databases.dbHandler import DbHandler


'''
This class deals with:
1. Training the model with images of individuals in the particular class against their name.
2. Identifying people found unmasked by using the aforementioned model.
'''

class MyFda:

    myPath = r'Face/Calculation/'

    def __init__(self, name):
        self.name = name

    def inputImgDataset(self):		#Obtaining and storing multiple images of individuals for training
        name = self.name
        status = False
        with open(r'Face\ValPairTable\combinations.csv', 'r') as f:
            rowsList = f.readlines()
            id = int(rowsList[-1].split(',')[0]) + 1

        thisEntry = [id, name]

        with open(r'Face\ValPairTable\combinations.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(thisEntry)

        cam = cv2.VideoCapture(0)
        time.sleep(2.0)

        observer = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        sampleSize = 0

        tempStorage = r'Face\Calculation\ ' + str(id)
        if not os.path.isdir(tempStorage):
            os.makedirs(tempStorage)

        while True:
            rect, img = cam.read()
            washed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face = observer.detectMultiScale(washed, 1.3, 5)
            for (x, y, w, h) in face:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleSize += 1
                cv2.imwrite(tempStorage + r'\ ' + str(sampleSize) + ".jpg", washed[y:y + h, x:x + w])
                print(str(sampleSize) + " Saved")
                cv2.imshow('Registering Faces', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif sampleSize >= 100:
                break
        status = True
        cv2.destroyAllWindows()
        return status

    def trainImgDataset(self):

        identifier = cv2.face.LBPHFaceRecognizer_create()
        ModelTrainingStatus = True
        ModelSaveStatus = True
        try:
            myFace, myId = self.assocImgLabel(self.myPath)
            identifier.train(myFace, np.array(myId))
        except:

            ModelTrainingStatus = False

        try:
            identifier.save(r'TrainingImageLabel/Trainner.yml')
        except:
            ModelSaveStatus = False

        return ModelTrainingStatus, ModelSaveStatus

    def assocImgLabel(self, path):
        observer = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        imgPath = []
        for everyFolder in os.listdir(path):
            for everyImg in os.listdir(os.path.join(path, everyFolder)):
                imgPath.append(os.path.join(os.path.join(path, everyFolder), everyImg))

        sampleImgs = []  # FaceSample
        sampleIds = []
        for eachPath in imgPath:

            thisImg = Image.open(eachPath).convert('L')
            imgArray = np.array(thisImg, 'uint8')
            faceInImg = observer.detectMultiScale(imgArray)

            eachId = int(os.path.split(eachPath)[-2].split("/")[-1])

            for (x, y, w, h) in faceInImg:
                sampleImgs.append(imgArray[y:y + h, x:x + w])
                sampleIds.append(eachId)

        return sampleImgs, sampleIds

    def identification(self):		#Called after unmasked person detected to identify them.

        global personId, person

        identifier = cv2.face.LBPHFaceRecognizer_create()
        identifier.read(r'Face/TrainingImageLabel/Trainner.yml')

        myCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_PLAIN
        found = 0

        file = open(r'Face\ValPairTable\combinations.csv', 'r')
        rowsList = file.readlines()
        while True:

            rect, img = cam.read()
            washed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            myTestFace = myCascade.detectMultiScale(washed, 1.2, 5)
            limiter = 0
            for (x, y, w, h) in myTestFace:
                limiter += 1
                predId, predScore = identifier.predict(washed[y:y + h, x:x + w])
                cv2.imshow("Scanning...", img)

                if predScore > 30:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 260, 0), 7)
                    predData = str(rowsList[predId].split(',')[1]) + " Accuracy: " + str('{:.3f}'.format(predScore))
                    cv2.putText(img, predData, (x, y - 50), font, 1, (0, 0, 255,), 2)

                    print(str(rowsList[predId].split(',')[1]), end=' ')
                    print(" Accuracy: " + str(predScore))

                    if predScore >70:
                        person = str(rowsList[predId].split(',')[1])
                        personId = predId
                        print("Person is: " + person)
                        '''HERE IS WHERE YOU PERFORM THE INSERTION TO THE DATABASE'''
                        found = 1
                        multiprocess = Thread(target=self.NoMaskEntry, args=(personId,person))
                        multiprocess.start()

                elif limiter==5:
                    person = "NNAT"
                    personId = "9999"
                    found = 1
                    break
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 260, 0), 7)
                    cv2.putText(img, "Identifying...", (x + h, y), font, 1, (255, 255, 0,), 4)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif found == 1:
                break
        try:
            cv2.destroyWindow("Scanning...")
        except:
            pass
        try:
            cv2.destroyWindow("Identifying...")
        except:
            pass



        file.close()
        return personId, person

    def NoMaskEntry(self, i, n):		#Writing the name of the identified unmasked person to the database
        handlerInstance = DbHandler(i, n)
        handlerInstance.write_db()
