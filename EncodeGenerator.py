import cv2
import face_recognition
import os
import pickle

# Folder where your student images are stored
path = 'Images'
images = []
student_ids = []

# Load all student images and IDs
for filename in os.listdir(path):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        img = cv2.imread(os.path.join(path, filename))
        images.append(img)
        student_ids.append(os.path.splitext(filename)[0])

print("Found", len(images), "images to encode.")

# Function to find encodings
def find_encodings(images_list):
    encode_list = []
    for image in images_list:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(image_rgb)
        if len(encodes) > 0:
            encode_list.append(encodes[0])
        else:
            print("⚠ Face not detected in one of the images.")
    return encode_list

print("Encoding images, please wait...")
encode_list_known = find_encodings(images)
encode_list_known_with_ids = [encode_list_known, student_ids]

# Save encoding data to pickle file
with open("EncodeFile.p", "wb") as file:
    pickle.dump(encode_list_known_with_ids, file)

print("✅ EncodeFile.p created successfully with", len(encode_list_known), "faces!")