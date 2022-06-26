import cv2
from fsdb.fsdb import Data, get_by_name
from settings import settings
import numpy as np
from faceapp.imagelables import imgsandlables


path = 'data'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml");


def train():
    faces, ids = imgsandlables(path, detector)
    recognizer.train(faces, np.array(ids))
    
    recognizer.save("recognizer.yml")
        
    return recognizer
            

# preparation

def register(name: str):
    
    # cam= cv2.VideoCapture(int(settings.CAM_PORT), cv2.CAP_DSHOW)
    cam= cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    new = Data(name)
    new.save()
    id = get_by_name(new.name).id
    
    count = 0
    while(True):
        _, img= cam.read()
        img= cv2.flip(img, 1) # Flip camera vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = detector.detectMultiScale(gray,1.6,5 )
        
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            count += 1
            cv2.imwrite(f"data/{id}.{str(count)}.jpg", gray[y:y+h,x:x+w])

        cv2.imshow('camera', img)
        k = cv2.waitKey(100) &  0xFF == ord('s')
        if k == 10:
            break
        elif count >= 50:
            print("Started training data")
            train()
            break
