
import os
from PIL import Image
from fsdb.fsdb import read_data
import base64
from io import BytesIO


path = "data"

def get_members():
    
    imagePaths = [os.path.join(path, i) for i in os.listdir(path) if i.endswith('.1.jpg')]
    members = read_data()
    
    try:
        for i in range(len(imagePaths)):
            image = Image.open(imagePaths[i])
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            members[i]['image'] = "data:image/jpeg;base64,"+img_str
    except:
        print("Failedd to load images")
        print(len(members), len(imagePaths))
            
    return members
