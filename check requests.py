import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDXRu2omq3p2KBfoj-0wj0iQ2kKnT60Jp8",
    "authDomain": "restroomsignout-bbcaf.firebaseapp.com",
    "projectId": "restroomsignout-bbcaf",
    "databaseURL": "https://restroomsignout-bbcaf-default-rtdb.firebaseio.com/",
    "storageBucket": "restroomsignout-bbcaf.appspot.com",
    "messagingSenderId": "120464602127",
    "appId": "1:120464602127:web:721a35455fd0c431fbdf7a",
    "measurementId": "G-JTHT4M7KE0"
}

firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()

ino = {"Grade": "Grade 7"}
database.child("Users_Login").child("Bowal").set(ino)