import face_recognition
from PIL import Image
import os

# Path to the database folder containing group images
database_folder = "present"
# Path to the erase folder to save segmented faces
erase_folder = "people"

# Ensure the "erase" folder exists, create it if not
if not os.path.exists(erase_folder):
    os.makedirs(erase_folder)

# Loop through each image in the "database" folder
for image_file in os.listdir(database_folder):
    # Construct the full path to the image
    image_path = os.path.join(database_folder, image_file)

    # Check if it's a file and not a directory
    if os.path.isfile(image_path) and image_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        try:
            # Load the image from the database
            image = face_recognition.load_image_file(image_path)
            # Find face locations for the current image
            face_locations = face_recognition.face_locations(image)
            
            print(f"I found {len(face_locations)} face(s) in {image_file}")

            # Save each detected face in "erase" folder
            for i, face_location in enumerate(face_locations):
                top, right, bottom, left = face_location
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                save_path = os.path.join(erase_folder, f"{image_file[:-4]}_face-{i+1}.jpg")
                pil_image.save(save_path)
                print(f"Saved {image_file[:-4]}_face-{i+1}.jpg")
                
        except Exception as e:
            print(f"Error processing {image_file}: {e}")
    else:
        print(f"{image_file} is not a valid image file.")
