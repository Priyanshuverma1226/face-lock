import cv2
import pickle
import face_recognition
import os
import cvzone
import numpy as np
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(3,480)

file=open('EncodeFile.p','rb')
encodeListKnownWithIds=pickle.load(file)
file.close()
encodeListKnown ,studentid=encodeListKnownWithIds

# print(studentid)

modeType=0
counter=0
id=-1
imgStudent=[]
while True:
    success,img=cap.read()
    
    imgs=cv2.resize(img,(0,0),None,0.25,0.25)
    imgs=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
     
    faceCurFrame=face_recognition.face_locations(imgs)
    encodeCurFrame=face_recognition.face_encodings(imgs,faceCurFrame)
    
    
    if faceCurFrame:
         for encodeface,faceloc in zip(encodeCurFrame,faceCurFrame):
                matches=face_recognition.compare_faces(encodeListKnown,encodeface)
                facedis=face_recognition.face_distance(encodeListKnown,encodeface)
                # print(matches)

                matchIndex=np.argmin(facedis)
                # print(matchIndex)
                if matches[matchIndex]:
                    print("Known Face Detected")
                    print(studentid[matchIndex])
                    y1, x2, y2, x1 = faceloc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                  
                    id = studentid[matchIndex]
                    id = studentid[matchIndex]
                    print(id)
                
    cv2.imshow("Result",img)
    cv2.waitKey(1)
    