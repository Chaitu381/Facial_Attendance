import cv2
import os
import time
import csv
import numpy as np
import face_recognition
from PIL import Image
from datetime import datetime

path = 'present'
database_path = 'database'
erase_folder = "people"

# cap = cv2.VideoCapture(0)
# img_counter = 1

# window_name = 'Live Video'
# cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
# try:
#     while True:
#         # Capture a frame from the camera
#         ret, frame = cap.read()
#         small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#         rgb_small_frame = small_frame[:, :, ::-1]

#         if ret:
#             cv2.imshow(window_name, frame)
#         # Generate a unique filename based on the current timestamp
#         timestamp = time.strftime("%H%M%S")
#         filename = f"{path}/image_{img_counter}.jpg"

#         # Save the captured frame to the specified file
#         cv2.imwrite(filename, frame)

#         print(f"Image capturing: {filename}")

#         # Wait for 5 minutes before capturing the next image
#         time.sleep(5)

#         img_counter += 1
#         if img_counter >= 6:
#             break
# except KeyboardInterrupt:
        
#     # If you manually stop the script (e.g., by pressing Ctrl+C), release the camera
#     cap.release()
#     print("Camera released.")


    
# #Release the camera when the script is done
# cap.release()


#face segmentation
for image_file in os.listdir(path):
    # Construct the full path to the image
    image_path = os.path.join(path, image_file)

    # Check if it's a file and not a directory
    if os.path.isfile(image_path) and image_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        try:
            # Load the image from the database
            image = face_recognition.load_image_file(image_path)
            # Find face locations for the current image
            face_locations = face_recognition.face_locations(image)
            
            print(f"I found {len(face_locations)} face in {image_file}")

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
        print("\n")
    else:
        print(f"{image_file} is not a valid image file.")


# Initialize person count
person_count = 0

# List of image files in the "database" folder
database_images = [f for f in os.listdir(database_path) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# Loop through each person's image in the "database" folder
for database_image_file in database_images:
    # Increment person count
    person_count += 1
    print(f"Person-{person_count}-=>{database_image_file}")
    
    # Construct the full path to the person's image in the "database" folder
    database_image_path = os.path.join(database_path, database_image_file)
    
    # Load the person's image and extract face encodings
    database_image = face_recognition.load_image_file(database_image_path)
    database_face_encodings = face_recognition.face_encodings(database_image)
    
    if len(database_face_encodings) > 0:
        compare1 = database_face_encodings[0]
    else:
        print(f"No faces found in {database_image_file}.")
        continue
    
    # List of image files in the "present" folder
    present_images = [f for f in os.listdir(erase_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    # Loop through each image in the "present" folder
    for present_image_file in present_images:
        # Construct the full path to the image in the "present" folder
        present_image_path = os.path.join(erase_folder, present_image_file)
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
       
# List of names in the "database" folder
database_names = [os.path.splitext(name)[0] for name in os.listdir(database_path)]
database_names1 = [os.path.splitext(name)[0] for name in os.listdir(path)]

# Initialize a set to store unique names
unique_names = set()

# Create and open the CSV file for writing
with open('attendance.csv', mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Write headers for Name, Time, and dynamic columns for attendance marks
    headers = ['Name', 'Time'] + [f'Mark-{i}' for i in range(1, len(database_names1) + 1)]
    writer.writerow(headers)

    # Initialize a dictionary to keep track of attendance count for each person
    attendance_count = {name: [0] * len(database_names1) for name in database_names}

    # Loop through each image in the "present" folder
    for index, present_image_file in enumerate(os.listdir(erase_folder), start=1):
        # Construct the full path to the image in the "present" folder
        present_image_path = os.path.join(erase_folder, present_image_file)
        try:
            # Open the image file
            with Image.open(present_image_path) as img:
                # Convert the image to RGB format explicitly
                img = img.convert("RGB")
                # Convert PIL image to NumPy array
                img_array = np.array(img)
                # Extract face encodings for the current image
                face_encodings = face_recognition.face_encodings(img_array)

                if len(face_encodings) > 0:
                    # Loop through each detected face
                    for face_encoding in face_encodings:
                        # Compare the face encoding with encodings in the "database" folder
                        for i, database_image_file in enumerate(os.listdir(database_path), start=1):
                            # Get the name of the person from the file name
                            person_name = os.path.splitext(database_image_file)[0]
                            # Load the person's image and extract face encodings
                            database_image_path = os.path.join(database_path, database_image_file)
                            database_image = face_recognition.load_image_file(database_image_path)
                            database_face_encodings = face_recognition.face_encodings(database_image)
                            
                            if len(database_face_encodings) > 0:
                                # Compare the face encodings
                                match = face_recognition.compare_faces([database_face_encodings[0]], face_encoding)
                                if match[0]:
                                    # Increment attendance count for the matched person
                                    attendance_count[person_name][index - 1] += 1

        except Exception as e:
            # Handle any exceptions (e.g., file not found)
            print(f"Error processing {present_image_file}: {e}")

    # Write attendance data to the CSV file
    for person_name, counts in attendance_count.items():
        current_time = datetime.now().strftime('%H:%M:%S')
        row = [person_name, current_time] + counts
        writer.writerow(row)

print("Attendance data saved to attendance.csv")