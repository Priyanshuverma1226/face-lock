import cv2
import face_recognition
import os
import pickle

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("my.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://cvzone-e7c2c-default-rtdb.firebaseio.com/",
    'storageBucket':"cvzone-e7c2c.appspot.com"
})


folderPath="Images"
pathlist=os.listdir(folderPath)
imgList=[]
studentid=[]


for path in pathlist:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    # print(os.path.splitext(path)[0])
    studentid.append(os.path.splitext(path)[0])

    
    fileName = f'{folderPath}/{path}'
    print(fileName)
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

# print(len(imgList)) 
# print(studentid)







def findEncodings(imageslist):
    encodeList = []
    for img in imageslist:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        
    return encodeList

encodeListKnown= findEncodings(imgList)
encodeListKnownWithIds=[encodeListKnown ,studentid]
print(encodeListKnown)


file=open('EncodeFile.p','wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()