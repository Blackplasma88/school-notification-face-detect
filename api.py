from fastapi import FastAPI, File, UploadFile
import shutil
import os
import face_recognition
import pickle
from typing import List
import requests
import face_detect

apiKey = "dKi3C4CBEMMmhg1TKUhp7z52gYVnURfahmz3n03vnHums0x6ciJVRy4YvSFKu2sZVtAvsFOgwrPXZFFOpaOKGXdeEuBvpMoVinBjUsXxYeUrfA8TmfxJPunlxCaGsSnGbPVfPTJRfywdalaXJmOqVBBh8LO8xEG16m829uqmO6HjqFUbfNmZZdZtGKj5PSPKs90Jc8L28iUBiiNOQNQI8vf1hxRrjKu2LXGtvqgU4FJ8b3Avtu6YcWB192QAzsPw"
app = FastAPI()


@app.post("/upload-image")
async def uploadImage(files: List[UploadFile] = File(...), class_id: str = "", student_id: str = "",id:str=""):
    if class_id == "":
        return {"msg": "require class_year"}
    if student_id == "":
        return {"msg": "require student_id"}

    if not (os.path.exists('dataset')):
        os.makedirs('dataset')
    if not (os.path.exists('dataset/'+class_id)):
        os.makedirs('dataset/'+class_id)
    if not (os.path.exists('dataset/'+class_id+'/'+student_id)):
        os.makedirs('dataset/'+class_id+'/'+student_id)

    pathImageList = []
    path = 'dataset/'+class_id+'/'+student_id
    for img in files:
        imageSplit = img.filename.split('.')
        imageFileExtension = imageSplit[len(imageSplit)-1]
        os.listdir(path)
        filename = student_id+'_' + \
            str(len(os.listdir(path))+1)+'.'+imageFileExtension
        pathImage = path+'/'+filename
        with open(pathImage, 'wb') as buffer:
            shutil.copyfileobj(img.file, buffer)
        pathImageList.append(pathImage)

    payload = {
        "id": id,
        "student_id": student_id,
        "image_path_list": pathImageList,
    }
    print(payload)
    headers = {"Content-Type": "application/json","Authorization": apiKey}
    resp = requests.post("http://127.0.0.1:8080/face-detection/upload-image-data",json=payload, headers=headers)
    print(resp.status_code)
    if resp.status_code != 200:
        print(resp.json()["message"])

    return {"msg": "upload success", "total_upload": len(files), "total_image": len(os.listdir(path))}


@app.post("/train-model")
async def trainModel(class_id: str):
    if class_id == "":
        return {"msg": "require class_year"}

    known_faces = []

    if not (os.path.exists('dataset')):
        print("dir dataset not exists")
        return {"msg": "dir dataset not exists"}
    if not (os.path.exists('dataset/'+class_id)):
        print("dir class id in dataset not exists")
        return {"msg": "dir class id in dataset not exists"}

    path = 'dataset/'+class_id

    if len(os.listdir(path)) == 0:
        return {"msg": "no dir profile data"}
    for dirName in os.listdir(path):
        print("dir image of student id:", dirName)
        if len(os.listdir(path+"/"+dirName)) <= 0:
            return {"msg": "no image profile data in dir student id: +"+dirName}
        for filename in os.listdir(path+"/"+dirName):
            # print(dirName+":"+filename)
            known_faces.append([dirName, path+"/"+dirName+"/"+filename])

    # print(known_faces)
    known_face_names = []
    known_face_encodings = []

    for face in known_faces:
        known_face_names.append(face[0])
        face_image = face_recognition.load_image_file(face[1])
        face_encoding = face_recognition.face_encodings(face_image)[0]
        known_face_encodings.append(face_encoding)

    if not (os.path.exists('models')):
        os.makedirs('models')
    if not (os.path.exists('models/'+class_id)):
        os.makedirs('models/'+class_id)
    pickle.dump((known_face_names, known_face_encodings), open(
        'models/'+class_id+"/"+class_id+'-faces.p', 'wb'))
    
    payload = {
        "id": id,
    }
    print(payload)
    headers = {"Content-Type": "application/json","Authorization": os.getenv("APIKEY")}
    resp = requests.post("http://127.0.0.1:8080//face-detection/trained-model",json=payload, headers=headers)
    print(resp.status_code)
    if resp.status_code != 200:
        print(resp.json()["message"])

    return {"msg": "success"}


@app.get("/cv")
async def openCV(course_id:str = "",class_id:str = ""):
    face_detect.faceDetect(class_id,course_id)
    
    return {}
