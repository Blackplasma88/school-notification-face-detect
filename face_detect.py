import face_recognition
import numpy
import cv2
import pickle
import call_api

def faceDetect(class_id,course_id):
    print("class_id",class_id)
    print("course_id",course_id)
    cap = cv2.VideoCapture(0)

    face_locations = []
    face_encodings = []
    process_frame = True
    color_found = [0,255,0]
    font = cv2.FONT_HERSHEY_DUPLEX

    path_face_model = "models/"+class_id+"/"+class_id+"-"
    known_face_names , known_face_encodings = pickle.load(open(path_face_model+'faces.p','rb'))

    while True:
        ret,frame = cap.read()

        if ret:
            smallFrame = cv2.resize(frame,(0,0),fx=0.5,fy=0.5)

            face_names = []
            face_percent = []

            # process
            if process_frame:
                face_locations = face_recognition.face_locations(smallFrame)
                face_encodings = face_recognition.face_encodings(smallFrame,face_locations)
                for face_encoding in face_encodings:
                    face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
                    best_index = numpy.argmin(face_distances)
                    face_percent_value = 1-face_distances[best_index]

                    if face_percent_value >= 0.6:
                        name = known_face_names[best_index]
                        percent = round(face_percent_value*100,2)
                        face_percent.append(percent)
                        call_api.call(name, course_id,class_id)
                    else:
                        name = "Unknown"
                        face_percent.append(0)

                    face_names.append(name)

            # draw and put text
            for (top,right,bottom,left), name, percent in zip(face_locations,face_names,face_percent):
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                if name != "Unknown":
                    #print(name+" : "+str(top)+" : "+str(right)+" : "+str(bottom)+" : "+str(left))
                    cv2.rectangle(frame, (left,top), (right,bottom), color_found, 2)
                    cv2.rectangle(frame,(left-1,top-20), (right+1,top), color_found, cv2.FILLED)
                    cv2.rectangle(frame,(left-1,bottom), (right+1,bottom+30), color_found, cv2.FILLED)

                    cv2.putText(frame,name,(left+6,top-6),font,0.6,(255,255,255),1)
                    cv2.putText(frame,"match: "+str(percent)+"%",(left+6,bottom+23),font,0.6,(255,255,255),1)

            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            break

    cap.release()
    cv2.destroyAllWindows()