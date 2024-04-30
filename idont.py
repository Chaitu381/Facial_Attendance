import cv2
import numpy as np
import face_recognition
import os
from PIL import Image

# Load images from the database
database_folder = 'database'
database_images = [f for f in os.listdir(database_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
database_face_encodings = []

for image_file in database_images:
    image_path = os.path.join(database_folder, image_file)
    try:
        with Image.open(image_path) as img:
            img_array = np.array(img)
            face_encoding = face_recognition.face_encodings(img_array)[0]
            database_face_encodings.append(face_encoding)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

# Initialize the video capture
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the live video
    ret, frame = cap.read()

    # Find face locations and encodings in the live frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        # Compare with each face in the database
        results = face_recognition.compare_faces(database_face_encodings, face_encoding)
        
        for i, result in enumerate(results):
            if result:
                print(f"Person {i + 1} is present in the live video.")

    # Display the live video frame
    cv2.imshow('Live Video', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
