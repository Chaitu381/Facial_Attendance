import numpy as np
import face_recognition
from PIL import Image
import os

database_path = 'database'
path = 'people'

# Load the image from the database for comparison
database_image_path = 'database/Chaitanya.jpg'
database_image = face_recognition.load_image_file(database_image_path)
database_face_encodings = face_recognition.face_encodings(database_image)

if len(database_face_encodings) > 0:
    compare1 = database_face_encodings[0]
else:
    print("No faces found in the database image.")

# List of image files in the "present" folder
image_files = [f for f in os.listdir(path) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# Loop through each image in the "present" folder
for image_file in image_files:
    # Construct the full path to the image in the "present" folder
    image_path = os.path.join(path, image_file)
    try:
        # Open the image file
        with Image.open(image_path) as img:
            # Convert PIL image to NumPy array
            img_array = np.array(img)

            # Extract face encodings for the current image
            face_encodings = face_recognition.face_encodings(img_array)

            if len(face_encodings) > 0:
                compare2 = face_encodings[0]

                # Compare the face encodings
                result = face_recognition.compare_faces([compare1], compare2)

                # Print the result (present or absent)
                if result[0]:
                    print(f"{image_file}: Present")
                else:
                    print(f"{image_file}: Absent")
            else:
                print(f"{image_file}: No face found in the image")

    except Exception as e:
        # Handle any exceptions (e.g., file not found)
        print(f"Error processing {image_path}: {e}")
