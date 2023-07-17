import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("my.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://cvzone-e7c2c-default-rtdb.firebaseio.com/"
})

ref=db.reference('students')

data={
    "122620":
        {
            "Name":"Priyanshu  verma",
            "Major":"Ai Engineer",
            "starting_year":2020,
            "total_attendance":6,
            "standing":'G',
            "year":4,
            "last_attendance_time":"2023-06-23 7:59:34",
            
        }
}

for key,value in data.items():
    ref.child(key).set(value)