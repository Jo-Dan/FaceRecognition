"""
Live webcam face recognition; By Jo-dan
"""
import time
import csv
import numpy as np
import cv2
from PIL import Image
#my functions
import faceframes
import getlab
import my_IFTTT
#webcam number
Camera_Number = 2
vc = cv2.VideoCapture(Camera_Number)
#paths
face_database = 'yalefaces'
cascadepath = "haarcascade_frontalface_default.xml"
facecascade = cv2.CascadeClassifier(cascadepath)
log_file = open('live_log.txt', 'a')
#colours
admin_colour = (255, 000, 000)
user_colour = (58, 238, 247)
unknown_colour = (000, 000, 255)
threat_colour = (000, 000, 255)
back_colour = (255, 255, 255)
#font of text on video
font = cv2.FONT_HERSHEY_SIMPLEX

recognizer = cv2.face.createLBPHFaceRecognizer()
#load subject database
timenow = time.strftime("%d/%m/%Y") + ' - ' + time.strftime("%I:%M:%S")
log_file.write('\nInitialised at {}. \n'.format(timenow))
with open('subjects.csv', "rb") as subjects:
    reader = csv.reader(subjects)
    subject_name = []
    subject_type = []
    for row in reader:
        subject_name.append(row[1])
        if len(row[2]) == 0:
            subject_type.append('UNKNOWN')
        else:
            subject_type.append(row[2])
    subject_name = [x.upper() for x in subject_name]
    subject_type = [x.upper() for x in subject_type]
    log_file.write('   CSV Read. \n')
# webcam; change this number 0~5 if webcam not working

def normal_subject_path(a):
    normface = face_database + "/subject{}.normal".format(str(a).zfill(2))
    normopen = Image.open(normface)
    normnp = np.array(normopen, 'uint8')
    return normnp

def load_data():
    database = raw_input("Would you like to (r)ebuild, or (l)oad the database?")
    if str(database) == 'r':
        images, labels = getlab.get_images_and_labels(face_database)
        cv2.destroyAllWindows()
        recognizer.train(images, np.array(labels))
        recognizer.save('trainingsaved')
        log_file.write('   Recognizer Retrained \n')
    elif str(database) == 'l':
        recognizer.load('trainingsaved')
        log_file.write('   Recogniser Training Loaded \n')
    else:
        load_data()

    cv2.destroyAllWindows()
shape_type = raw_input("(b)oxes, (c)circles, (p)oi or (s)amaritan?")
log_file.write('   Run in "{}" Mode. \n'.format(shape_type))
load_data()

nbr_old = 0
nbr_predicted = 0

if shape_type == 'p':
    admin_colour = (58, 238, 247)
    analog_colour = (58, 238, 247)
    user_colour = (243, 124, 13)
    unknown_colour = (255, 255, 255)
    threat_colour = (000, 000, 255)
    back_colour = (000, 000, 000)
    

while True:
        #read frame by frame
        ret, frame = vc.read()
        #cv2.imshow('stream', frame)
        admin_present = False
        user_present = False
        unknown_present = False
        threat_present = False
        analog_present = False
        grey_predict = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        predict_image = np.array(grey_predict, 'uint8')
        faces = facecascade.detectMultiScale(predict_image, 1.03, 5, 0, (150, 150))
        for (x, y, h, w) in faces:
            nbr_predicted = recognizer.predict(predict_image[y:y+h, x:x+w])
            #strings for stream
            subtxt = "Subject: {}".format(nbr_predicted)
            nametxt = "Name: {}".format(subject_name[nbr_predicted])
            typetxt = "Type: {}".format(subject_type[nbr_predicted])

            #Text on stream
            if subject_type[nbr_predicted] == 'ADMIN':
                all_colour = admin_colour
                admin_present = True
            elif subject_type[nbr_predicted] == 'USER':
                all_colour = user_colour
                user_present = True
            elif subject_type[nbr_predicted] == 'UNKNOWN':
                all_colour = unknown_colour
                unknown_present = True
            elif subject_type[nbr_predicted] == "THREAT":
                all_colour = threat_colour
                threat_present = True
            elif subject_type[nbr_predicted] == "ANALOG":
                all_colour = analog_colour
                analog_present = True

            if shape_type == 'c':
                cv2.circle(frame, (x+int(round(.5*w)), y+int(round(.5*h))), int(round(.6*h)), all_colour, 4)
                subco = (x+w+30, y+int(round(.5*h))-25)
                nameco = (x+w+30, y+int(round(.5*h)))
                typeco = (x+w+30, y+int(round(.5*h))+25)
            elif shape_type == 'p':
                faceframes.poi_box(frame, x, y, w, h, subject_type[nbr_predicted])
                subco = (x, y+h+25)
                nameco = (x, y+h+50)
                typeco = (x, y+h+75)
            elif shape_type == 's':
                faceframes.sam_circle(frame, x, y, w, h, subject_type[nbr_predicted])
                subco = (x+w+30, y+int(round(.5*h))-25)
                nameco = (x+w+30, y+int(round(.5*h)))
                typeco = (x+w+30, y+int(round(.5*h))+25)
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), all_colour, 2)
                txt_x = x
                subco = (x, y+h+25)
                nameco = (x, y+h+50)
                typeco = (x, y+h+75)

            cv2.putText(frame, subtxt, subco, font, .7, back_colour, 3)
            cv2.putText(frame, subtxt, subco, font, .7, all_colour, 2)
            cv2.putText(frame, nametxt, nameco, font, .7, back_colour, 3)
            cv2.putText(frame, nametxt, nameco, font, .7, all_colour, 2)
            cv2.putText(frame, typetxt, typeco, font, .7, back_colour, 3)
            cv2.putText(frame, typetxt, typeco, font, .7, all_colour, 2)

            cv2.imshow('stream', frame)

            if nbr_predicted != nbr_old:
                print "Recognized as {}".format(nbr_predicted)
                #my_IFTTT.IFTTT('Face_Detected', subject_type[nbr_predicted], subject_name[nbr_predicted], str(Camera_Number))
                log_file.write('      Subject {} recognised:  {} \n'.format(nbr_predicted, subject_type[nbr_predicted]))
                recognp = normal_subject_path(nbr_predicted)
                cv2.imshow("Recognised as...", recognp)
    #            oldnp = normal_subject_path(nbr_old)
    #            cv2.imshow("Previous", oldnp)
                nbr_old = nbr_predicted

        if threat_present == True:
            cv2.putText(frame, 'THREAT DETECTED', (0, 25), font, 1, back_colour, 5)
            cv2.putText(frame, 'ACCESS: DENIED', (0, 50), font, 1, back_colour, 5)
            cv2.putText(frame, 'THREAT DETECTED', (0, 25), font, 1, threat_colour, 2)
            cv2.putText(frame, 'ACCESS: DENIED', (0, 50), font, 1, threat_colour, 2)
        elif analog_present == True:
            cv2.putText(frame, 'ANALOG INTERFACE DETECTED', (0, 25), font, 1, back_colour, 5)
            cv2.putText(frame, 'ACCESS: GRANTED', (0, 50), font, 1, back_colour, 5)
            cv2.putText(frame, 'ANALOG INTERFACE DETECTED', (0, 25), font, 1, analog_colour, 2)
            cv2.putText(frame, 'ACCESS: GRANTED', (0, 50), font, 1, analog_colour, 2)
        elif admin_present == True:
            cv2.putText(frame, 'ADMIN DETECTED', (0, 25), font, 1, back_colour, 5)
            cv2.putText(frame, 'ACCESS: GRANTED', (0, 50), font, 1, back_colour, 5)
            cv2.putText(frame, 'ADMIN DETECTED', (0, 25), font, 1, admin_colour, 2)
            cv2.putText(frame, 'ACCESS: GRANTED', (0, 50), font, 1, admin_colour, 2)
        elif user_present == True:
            cv2.putText(frame, 'USER DETECTED', (0, 25), font, 1, back_colour, 5)
            cv2.putText(frame, 'ACCESS: RESTRICTED', (0, 50), font, 1, back_colour, 5)
            cv2.putText(frame, 'USER DETECTED', (0, 25), font, 1, user_colour, 2)
            cv2.putText(frame, 'ACCESS: RESTRICTED', (0, 50), font, 1, user_colour, 2)
        elif unknown_present == True:
            cv2.putText(frame, 'UNKNOWN USER', (0, 25), font, 1, back_colour, 5)
            cv2.putText(frame, 'ACCESS: DENIED', (0, 50), font, 1, back_colour, 5)
            cv2.putText(frame, 'UNKNOWN USER', (0, 25), font, 1, unknown_colour, 2)
            cv2.putText(frame, 'ACCESS: DENIED', (0, 50), font, 1, unknown_colour, 2)
        
        if nbr_old != 0 and len(faces) == 0:
            print 'No face in frame.'
            nbr_old = 0

        cv2.imshow('stream', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
vc.release()

cv2.destroyAllWindows()

timenow = time.strftime("%d/%m/%Y") + ' - ' + time.strftime("%I:%M:%S")
log_file.write('Program Terminated at {}. \n'.format(timenow))
print '.......\nGoodbye \n.......'
