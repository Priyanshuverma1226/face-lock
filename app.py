from flask import * 
import cv2
app = Flask(__name__)

import numpy as np

import pickle
import face_recognition

import os
import cvzone


file=open('EncodeFile.p','rb')
encodeListKnownWithIds=pickle.load(file)
file.close()
encodeListKnown ,studentid=encodeListKnownWithIds




def generate_frames():
    
    counter =0
    while True:
        
       
        success,img=camera.read()
       
        imgs=cv2.resize(img,(0,0),None,0.25,0.25)
        imgs=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
           
        faceCurFrame=face_recognition.face_locations(imgs)
        encodeCurFrame=face_recognition.face_encodings(imgs,faceCurFrame)
        if faceCurFrame:
            
            
            for encodeface,faceloc in zip(encodeCurFrame,faceCurFrame):
                matches=face_recognition.compare_faces(encodeListKnown,encodeface)
                facedis=face_recognition.face_distance(encodeListKnown,encodeface)
                matchIndex=np.argmin(facedis)
                
                if matches[matchIndex]:
                    print("Face Detected")
                    
                    counter = counter + 1
                    if counter ==5:
                        with open('n.txt' ,'w') as f:
                            f.write("True")

                matchIndex=np.argmin(facedis)
    
        ret,buffer=cv2.imencode('.jpg',img)
        img=buffer.tobytes()
        

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')









@app.route('/')
def hello_world():
    global camera
    global counter

    camera=cv2.VideoCapture(0)
    
    return render_template('index.html')



@app.route("/autoscan")
def scan():
    
    
    a = request.args.get('a')
    return render_template('scan.html')






@app.route('/video',methods = [ 'GET'])
def video():
    a = request.args.get('a')

    global objecti
    objecti=[]
    
    if a=='1':
        camera.release()
        with open('n.txt' , 'r') as f:
            k=f.read()
        with open('n.txt' , 'w') as f:
            f.write('')
            
            
        if k=='True':
            

      
        
            return render_template("detected.html")
        else :
             return render_template("fail.html")

    if a==None:
        
        return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
       
        return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
        

if __name__ == '__main__':
    
    app.run()