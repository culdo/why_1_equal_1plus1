# https://github.com/ageitgey/face_recognition
import numpy as np
import face_recognition
import cv2
import time
import os
from PIL import Image
from os import listdir
from os.path import isfile, isdir, join

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
known_face_names = [] #存放登錄相片名稱
known_face_encodings = []

def face_data(input):
    mypath = "C:/Users/user/Desktop/why_i_equal_i_plus_1/pictures"   # 指定要列出所有檔案的目錄
    files = listdir(mypath) # 取得所有檔案與子目錄名稱

    if(input == "show"):
        for f in files: # 以迴圈處理
          fullpath = join(mypath, f)    # 產生檔案的絕對路徑
          if isfile(fullpath):# 判斷 fullpath 是檔案還是目錄
            print("file：", f)
          # elif isdir(fullpath):
          #   print("目錄：", f)

    if (input == "add"):
        for f in files:  # 以迴圈處理
            fullpath = join(mypath, f)  # 產生檔案的絕對路徑
            if isfile(fullpath):  # 判斷 fullpath 是檔案還是目錄
                # print( f,"已加入data_name")
                known_face_names.append(f.rstrip(".jpg"))

def identification():
    print("按下 Enter 以離開")
    process_this_frame = True
    face_data("add") # 將照片名稱加入data_name
    name_count = np.zeros(len(known_face_names))

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    for i in range(0,len(known_face_names),1):
        # jpg_name = str(i)+".jpg"
        jpg_name = known_face_names[i]+".jpg"
        print("已將 '"+jpg_name+"' 加入辨識資料")
        # print(name_list[i-1])
        known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file("C:/Users/user/Desktop/why_i_equal_i_plus_1/pictures/"+jpg_name))[0])

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding,0.4)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2
    #===============================
            for name_index in range (0,len(known_face_names),1):
                if known_face_names[name_index] == name:
                    # print(known_face_names[name_index])
                    if name_count[name_index] == 0:
                        name_count[name_index] = 1
                        # print(name_count[name_index])
                        timestart =time.time()
                        # ttstart=time.time()
                        print(name)

                    else:
                        if (time.time()-timestart) > 10:
                            print(name)
                            # print(time.time()-timestart)
                        # elif (time.time()-ttstart) >
                            # timestart = time.time()
    #=====================================
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Face Recognition', frame)

        # Hit Enter on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('\r'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

def creat_data():
    print("請將臉部完整呈現在畫面中！")
    print("按下 Enter 以拍照！")
    process_this_frame = True
    video_capture = cv2.VideoCapture(0)
    while(True):
        ret, frame = video_capture.read()
        cv2.imshow('Face sign up', frame)
        if cv2.waitKey(1) & 0xFF == ord('\r'):
            picture_name = str(time.localtime().tm_year)+str(time.localtime().tm_mon)+str(time.localtime().tm_mday) \
                           +str(time.localtime().tm_hour)+str(time.localtime().tm_min)+str(time.localtime().tm_sec)+".jpg"
            cv2.imwrite("C:/Users/user/Desktop/why_i_equal_i_plus_1/org_pictures/"+picture_name, frame)
            # print("Picture {} has been saved successfully !".format(picture_name))
            break
    video_capture.release()
    cv2.destroyAllWindows()

    image = face_recognition.load_image_file("C:/Users/user/Desktop/why_i_equal_i_plus_1/org_pictures/"+picture_name)
    face_locations = face_recognition.face_locations(image)
    # print("I found {} face(s) in this photograph.".format(len(face_locations)))
    for face_location in face_locations:
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.show()
        name = input('請輸入照片中人物之英文姓名： ')
        pil_image.save("C:/Users/user/Desktop/why_i_equal_i_plus_1/pictures/"+name+".jpg")
        print(name," 的照片已成功加入資料庫！")
    os.remove("C:/Users/user/Desktop/why_i_equal_i_plus_1/org_pictures/"+picture_name)
    time.sleep(2)

def main():
    while(True):
        # cv2.VideoCapture(0).release()
        # cv2.destroyAllWindows()
        os.system("cls")
        state = input('歡迎使用此人臉辨識系統！\n1) 開始辨識 \n2) 新增人員\n3) 查看人員名單\n4) 離開\n請選擇想執行的動作： ')
        if(state == '1'):
            identification()
            continue
        elif(state == '2'):
            creat_data()
            continue
        elif (state == '3'):
            os.system("cls")
            face_data('show')
            if(input('\n按下 Enter 鍵返回主選單') == '\r'):
                continue
        elif (state == '4'):
            print("System shutdown！")
            time.sleep(2)
            break
        else:
            print("！！Input error！！")
            time.sleep(1)

main()