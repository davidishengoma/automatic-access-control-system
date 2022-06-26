
import os
from PIL import Image
import numpy as np

def imgsandlables(path, detector):
    imagePaths = [os.path.join(path, i) for i in os.listdir(path) if i != "data.md"]
    
    indfaces = []
    ids = []
    for imagePath in imagePaths:
        img = Image.open(imagePath).convert('L')  # grayscale
        imgnp = np.array(img, 'uint8')
        
        id = int(os.path.split(imagePath)[-1].split(".")[0])
        
        faces = detector.detectMultiScale(imgnp)
        for (x, y, w, h) in faces:
            indfaces.append(imgnp[y:y + h, x:x + w])
            ids.append(id)
    return indfaces, ids