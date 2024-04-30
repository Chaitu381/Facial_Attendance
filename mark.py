import os
import face_recognition
from PIL import Image
import numpy as np
import csv
from datetime import datetime

path = 'present'
database_path = 'database'
erase_folder = "people"

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
        row = [person_name, current_time] + [str(count) for count in counts]
        writer.writerow(row)

print("Attendance data saved to attendance.csv")