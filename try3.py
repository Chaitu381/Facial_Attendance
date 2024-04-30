import cv2
import time

# Path where images will be saved
path = 'images'

# Open the default camera (usually the laptop's built-in camera)
cap = cv2.VideoCapture(0)

# Counter for the images
img_counter = 1

# Name for the window displaying the video
window_name = 'Live Video'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

try:
    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()
        
        if ret:
            # Display the frame
            cv2.imshow(window_name, frame)
            
            # Generate a unique filename based on the current timestamp
            timestamp = time.strftime("%H%M%S")
            filename = f"{path}/image_{img_counter}.jpg"

            # Save the captured frame to the specified file
            cv2.imwrite(filename, frame)

            print(f"Image capturing: {filename}")

            # Wait for 5 seconds before capturing the next image
            key = cv2.waitKey(1)  # Wait for 1ms
            if key == 27:  # If ESC key is pressed, exit
                break

            img_counter += 1
            if img_counter >= 6:
                break

except KeyboardInterrupt:
    # If you manually stop the script (e.g., by pressing Ctrl+C), release the camera
    cap.release()
    print("Camera released.")

# Release the camera when the script is done
cap.release()
cv2.destroyAllWindows()  # Close all OpenCV windows
