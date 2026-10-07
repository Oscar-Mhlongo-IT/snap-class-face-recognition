import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import sqlite3
from datetime import datetime

# ---------------- DATABASE CONNECTION ---------------- #
def get_student_by_id(student_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students WHERE id = ?", (student_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def update_attendance(student_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE Students
        SET total_attendance = total_attendance + 1,
            last_attendance_time = ?
        WHERE id = ?
    """, (now, student_id))

    conn.commit()
    conn.close()

# ---------------- CAMERA SETUP ---------------- #
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

# ---------------- LOAD ENCODINGS ---------------- #
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")

# ---------------- VARIABLES ---------------- #
modeType = 0
counter = 0
id = -1
imgStudent = []

# ---------------- MAIN LOOP ---------------- #
while True:
    success, img = cap.read()
    if not success:
        print("Failed to access camera.")
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                id = studentIds[matchIndex]
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                studentInfo = get_student_by_id(id)
                if studentInfo:
                    print(f"Student found: {studentInfo[1]}")
                    last_time_str = studentInfo[6]
                    last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - last_time).total_seconds()

                    if secondsElapsed > 30:
                        update_attendance(id)
                        modeType = 2
                    else:
                        modeType = 3
                else:
                    print(f"Student ID {id} not found in database.")
                    modeType = 3

            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if counter <= 10 and studentInfo:
                cv2.putText(imgBackground, f"{studentInfo[1]}", (860, 445),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                cv2.putText(imgBackground, f"{studentInfo[2]}", (1006, 550),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgBackground, f"ID: {studentInfo[0]}", (860, 493),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgBackground, f"Year: {studentInfo[5]}", (910, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imgBackground, f"Attendance: {studentInfo[4]}", (1025, 125),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1)

            counter += 1
            if counter >= 20:
                counter = 0
                modeType = 0
                id = -1
    else:
        modeType = 0
        counter = 0

        cv2.imshow("Face Attendance", imgBackground)
        key = cv2.waitKey(1)
        if key == ord('q') or cv2.getWindowProperty("Face Attendance", cv2.WND_PROP_VISIBLE) < 1:
            print("Closing program...")
            break

    cap.release()
    cv2.destroyAllWindows()

