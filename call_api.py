import requests
import os
import datetime

urlServer = "http://localhost:8080"
apiKey = "dKi3C4CBEMMmhg1TKUhp7z52gYVnURfahmz3n03vnHums0x6ciJVRy4YvSFKu2sZVtAvsFOgwrPXZFFOpaOKGXdeEuBvpMoVinBjUsXxYeUrfA8TmfxJPunlxCaGsSnGbPVfPTJRfywdalaXJmOqVBBh8LO8xEG16m829uqmO6HjqFUbfNmZZdZtGKj5PSPKs90Jc8L28iUBiiNOQNQI8vf1hxRrjKu2LXGtvqgU4FJ8b3Avtu6YcWB192QAzsPw"


def call(id, course_id,class_id):
    
    if not (os.path.exists('status')):
        os.makedirs('status')

    if not (os.path.exists('status/'+class_id)):
        os.makedirs('status/'+class_id)

    if not (os.path.exists("status/"+class_id+"/status.txt")):
        file = open("status/"+class_id+"/status.txt", "w+")
    else:
        file = open("status/"+class_id+"/status.txt", "r+")
    
    for f in file:
        f = f[0:len(f)-1]
        # print(f)
        if f == id:
            print("yes")
            return "checked"
    
    # now = datetime.datetime.now()
    payload = {
    "course_id":course_id,
    "date":datetime.datetime.now().strftime("%Y-%m-%d"),
    "student_id":id,
    "check_by":"server"
    }
    print(payload)
    headers = {"Content-Type":"application/json","Authorization":apiKey}
    resp = requests.post(urlServer+"/check-name/student-check",json=payload,headers=headers) 
    print(resp)
    if resp.status_code >= 400:
        print("check name not success")
        print(resp.content())
        return False

    file.write(id+'\n')
    file.close()
    print("checked name")
    
    return True