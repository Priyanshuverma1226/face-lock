import cv2
import pickle
import face_recognition
cap=cv2.VideoCapture(0)
import os
import cvzone
# cap.set(3,1280)
# cap.set(3,720)
import numpy as np
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("my.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://cvzone-e7c2c-default-rtdb.firebaseio.com/",
    'storageBucket':"cvzone-e7c2c.appspot.com"
})

import numpy as np
cap.set(3,640)
cap.set(3,480)

p=0

imgBackground=cv2.imread("Resources/bg.png")


folderModePath="Resources/Modes"
modePathList=os.listdir(folderModePath)
imgModelist=[]


for path in modePathList:
    imgModelist.append(cv2.imread(os.path.join(folderModePath,path)))

print(len(imgModelist))


bucket = storage.bucket()



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
    
    
    
    imgBackground[162:162+480,55:55+640]=img
    imgBackground[44:44+633,808:808+414]=imgModelist[modeType]
    
    if faceCurFrame:
                
            for encodeface,faceloc in zip(encodeCurFrame,faceCurFrame):
                matches=face_recognition.compare_faces(encodeListKnown,encodeface)
                facedis=face_recognition.face_distance(encodeListKnown,encodeface)
                # print(matches)

                matchIndex=np.argmin(facedis)
                # print(matchIndex)
                if matches[matchIndex]:
                    # print("Known Face Detected")
                    # print(studentid[matchIndex])
                    y1, x2, y2, x1 = faceloc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    id = studentid[matchIndex]
                    id = studentid[matchIndex]
                    print(id)
                    if counter == 0:
                        
                        counter =1  
                        modeType=1
                        
            if counter != 0:
                if counter == 1:
                    studentInfo=db.reference(f'students/{id}').get()
                    print(studentInfo)
                    
                    blob=bucket.get_blob(f"Images/{id}.png")
                    array=np.frombuffer(blob.download_as_string(),np.uint8)
                    imgStudent=cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                    
                    k=studentInfo['last_attendance_time']
                    print(type(k))
                    datetimeObject=datetime.strptime(k,"%Y-%m-%d %H:%M:%S")
                    secondElapse=(datetime.now()-datetimeObject).total_seconds()
                    print(secondElapse)
                    
                    if secondElapse>15:
                        studentInfo['total_attendance'] +=1
                        ref=db.reference(f'students/{id}')    
                        ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        
                    else:
                        modeType=3
                        counter=0
                        imgBackground[44:44+633,808:808+414]=imgModelist[modeType]
                    
                   
                if modeType!=3:
                    

                    
                    if 10<counter<40:
                        modeType=2

                    imgBackground[44:44+633,808:808+414]=imgModelist[modeType]
                        
                        
                    if counter<=10:
                        cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                        cv2.putText(imgBackground,str(studentInfo['Name']),(920,445),cv2.FONT_HERSHEY_COMPLEX,0.5,(50,50,50),1)
                        cv2.putText(imgBackground,str(studentInfo['Major']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                        cv2.putText(imgBackground,str(id),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                        cv2.putText(imgBackground,str(studentInfo['standing']),(910,625),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                        cv2.putText(imgBackground,str(studentInfo['year']),(910,625),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                        imgBackground[175:175+216,909:909+216]=imgStudent
                        
                        
                counter+=1


                
                if counter>=40:
                    counter=0
                    modeType=0
                    studentInfo=[]
                    imgStudent=[]
                    imgBackground[44:44+633,808:808+414]=imgModelist[modeType]
                    
                    
                    
                    
            
            
    else:
        modeType=0       
        counter=0
        p=0
        imgBackground[44:44+633,808:808+414]=imgModelist[modeType]
        
    
    cv2.imshow("Result",imgBackground)
    cv2.waitKey(1)