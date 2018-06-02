import face_recognition
import cv2
from subprocess import Popen, PIPE, STDOUT
import os
Line = Popen(['ruby', 'test.rb'], stdin=PIPE, stdout=PIPE, stderr=STDOUT, bufsize=0)


def send_LINE(sendrb):
    Line.stdin.write(sendrb.encode())
        # Line.stdin.write(sendrb.encode())
        # result will be a list of lines:

    result = []
    # read slave output line by line, until we reach "[end]"
    while True:
        # check if slave has terminated:
        if Line.poll() is not None:
            print('slave has terminated.')
            exit()
        # read one line, remove newline chars and trailing spaces:
        line = Line.stdout.readline().rstrip().decode()
        # print('line:', line)
        if line == '[end]':
            break
        result.append(line)
    print('result:')
    print('\n'.join(result))


send_LINE("開始辨識\n")

known_face_encodings = []
known_face_names = [
    file.split('.')[0] for file in os.listdir() if file.endswith(".jpg")
]

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
#
# for i in range (1,len(known_face_names)+1,1):
#     jpg_name = str(i)+".jpg"
#     print(jpg_name)
#     # print(name_list[i-1])
#     known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(jpg_name))[0])
for fn in known_face_names:
    jpg_name = fn+".jpg"
    print(jpg_name)
    # print(name_list[i-1])
    known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(jpg_name))[0])

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
s2= "init"

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
            if face_encodings[-1] is face_encoding:
                s = list(zip(*list(zip(*face_locations)), face_names))
                if s2 != list(zip(*sorted(s,key=lambda k: k[3])))[-1]:

                    sendrb = "由左到右依序為"
                    for str in s2:
                        sendrb += ", " + str
                    sendrb += "\n"
                    print(sendrb)
                    send_LINE(sendrb)
                    s2 = list(zip(*sorted(s, key=lambda k: k[3])))[-1]

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()


