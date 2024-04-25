import face_recognition as fr
import cv2 as cv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from PIL import Image


Tk().withdraw
load_image = askopenfilename()
target_image = fr.load_image_file(load_image)
target_encoding = fr.face_encodings(target_image)
# print(target_encoding)

def encode_faces(folder):
    list_people_encoding = []
    for filename in os.listdir(folder):
        try:
            known_image = fr.load_image_file(f'{folder}/{filename}')
            face_encodings = fr.face_encodings(known_image)
            if face_encodings:
                known_encoding = face_encodings[0]  
                list_people_encoding.append((known_encoding, filename))
            else:
                print(f"No face found in {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    return list_people_encoding


def find_target_face():
    face_location = fr.face_locations(target_image)
    count = 0
    for person in encode_faces('C:/Users/Aarus/face/multiface/photos'):
        encoded_face = person[0]
        filename = person[1]
        is_target_face = fr.compare_faces(encoded_face, target_encoding, tolerance=0.55)
        print(f'{filename} is {is_target_face}')
        if face_location:
            face_number = 0
            for location in face_location:
                if is_target_face[face_number]:
                    label = filename
                    create_frame(location, label)
                    count+=1
                face_number+=1
    print("Total faces found: ", face_number)
# def find_target_face():
#     face_locations = fr.face_locations(target_image)
#     for location in face_locations:
#         create_frame(location, "Face")

def create_frame(location, label):
    top,right,bottom,left=location

    cv.rectangle(target_image, (left, top), (right, bottom), (255,0,0), 2)
    cv.rectangle(target_image, (left, bottom +20), (right, bottom), (255,0,0), cv.FILLED)
    cv.putText(target_image, label, (left+3, bottom+14), cv.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)

# def render_image():
#     rgb_img = cv.cvtColor(target_image, cv.COLOR_BGR2RGB)
#     cv.imshow('Face Recognition', rgb_img)
#     cv.imwrite("new_image.png", rgb_img)
#     cv.waitKey(0)
def render_image():
    # Resize the image to fit within a specific width and height
    max_width = 1500
    max_height = 1300
    scale = min(max_width / target_image.shape[1], max_height / target_image.shape[0])
    resized_image = cv.resize(target_image, None, fx=scale, fy=scale)

    rgb_img = cv.cvtColor(resized_image, cv.COLOR_BGR2RGB)
    cv.imshow('Face Recognition', rgb_img)
    cv.imwrite("new_image.png", rgb_img)
    cv.waitKey(0)


find_target_face()
render_image()



