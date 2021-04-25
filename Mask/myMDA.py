import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']="3"
import cv2
import imutils
import numpy as np
from imutils.video import VideoStream
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from Face.myFDA import MyFda

'''
This class deals with:
1. Detecting faces in the frame of the input video stream
2. Checking whether the said face is masked or not. (Note: Only white and grey masks are detected.)
3. If no mask is detected, FDA is called which recognises the unmasked face by their pre-input name
'''

class MyMDA:
    prototxtPath = r'Mask/face_detector/deploy.prototxt'
    weightsPath = r'Mask/face_detector/res10_300x300_ssd_iter_140000.caffemodel'
    faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

    maskNet = load_model(r'Mask/mask_detector.model')

    def __init__(self):
        print("")

    def detect_and_predict_mask(self, frame, faceNet, maskNet):

        # grab the dimensions of the frame and then construct a blob
        # from it
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

        # pass the blob through the network and obtain the face detections
        faceNet.setInput(blob)
        detections = faceNet.forward()

        # initialize our list of faces, their corresponding locations,
        # and the list of predictions from our face mask network
        faces = []
        locs = []
        preds = []


        for i in range(0, detections.shape[2]):

            confidence = detections[0, 0, i, 2]


            if confidence > 0.5:

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")


                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))


                face = frame[startY:endY, startX:endX]
                try:
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                    face = cv2.resize(face, (224, 224))
                    face = img_to_array(face)
                    face = preprocess_input(face)


                    faces.append(face)
                    locs.append((startX, startY, endX, endY))
                except Exception as e:
                    print(str(e))


        if len(faces) > 0:

            faces = np.array(faces, dtype="float32")

            preds = maskNet.predict(faces, batch_size=32)


        return locs, preds

    def ioMain(self):

        vs = VideoStream(src=0).start()
        time.sleep(2.0)

        while True:

            frame = vs.read()
            frame = imutils.resize(frame, width=400)

            (locs, preds) = self.detect_and_predict_mask(frame, self.faceNet, self.maskNet)

            for (box, pred) in zip(locs, preds):

                (startX, startY, endX, endY) = box
                (mask, withoutMask) = pred

                if mask > withoutMask:

                    label = "Mask Present"
                    color = (0, 255, 0)
                else:
                    frame = imutils.resize(vs.read(), width=400)
                    label = "No Mask Present!"
                    color = (0, 0, 255)

                    if withoutMask * 100 > 99.99:
                        vs.stop()
                        print("Mask Not detected!")
                        print("Identifying...")
                        Chk = MyFda("")			#Calling the FDA class to recognise the unmasked person
                        id, name = Chk.identification()
                        print("Identified and stored in Database...")
                        time.sleep(2.0)
                        vs = VideoStream(0).start()
                        print("vs restarted")


                label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

                cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)


            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF


            if key == ord("q"):
                break

        cv2.destroyAllWindows()
        vs.stop()
