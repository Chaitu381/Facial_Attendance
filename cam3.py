import cv2
import time

path = 'present'

cap = cv2.VideoCapture(0)
img_counter = 1

window_name = 'Live Video'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
try:
    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()
        if ret:
            cv2.imshow(window_name, frame)
        # Generate a unique filename based on the current timestamp
        timestamp = time.strftime("%H%M%S")
        filename = f"{path}/image_{img_counter}.jpg"

        # Save the captured frame to the specified file
        cv2.imwrite(filename, frame)

        print(f"Image capturing: {filename}")

        # Wait for 5 minutes before capturing the next image
        time.sleep(5)

        img_counter += 1
        if img_counter >= 6:
            break
except KeyboardInterrupt:
        
    # If you manually stop the script (e.g., by pressing Ctrl+C), release the camera
    cap.release()
    print("Camera released.")


    
#Release the camera when the script is done
cap.release()
