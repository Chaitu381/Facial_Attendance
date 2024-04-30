import os
from PIL import Image
import numpy as np
import face_recognition

# Path to the folder containing images of persons
database_folder = 'database'
# Path to the folder containing images to compare with database
present_folder = 'people'

# Initialize person count
person_count = 0

# List of image files in the "database" folder
database_images = [f for f in os.listdir(database_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# Loop through each person's image in the "database" folder
for database_image_file in database_images:
    # Increment person count
    person_count += 1
    print(f"Person-{person_count}-=>{database_image_file}")
    
    # Construct the full path to the person's image in the "database" folder
    database_image_path = os.path.join(database_folder, database_image_file)
    
    # Load the person's image and extract face encodings
    database_image = face_recognition.load_image_file(database_image_path)
    database_face_encodings = face_recognition.face_encodings(database_image)
    
    if len(database_face_encodings) > 0:
        compare1 = database_face_encodings[0]
    else:
        print(f"No faces found in {database_image_file}.")
        continue
    
    # List of image files in the "present" folder
    present_images = [f for f in os.listdir(present_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    # Loop through each image in the "present" folder
    for present_image_file in present_images:
        # Construct the full path to the image in the "present" folder
        present_image_path = os.path.join(present_folder, present_image_file)
        try:
            # Open the image file
            with Image.open(present_image_path) as img:
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
                        print(f"{database_image_file} vs {present_image_file}: Present")
                    else:
                        print(f"{database_image_file} vs {present_image_file}: Absent")
                else:
                    print(f"{present_image_file}: No face found in the image")

        except Exception as e:
            # Handle any exceptions (e.g., file not found)
            print(f"Error processing {present_image_file}: {e}")
    print("\n")