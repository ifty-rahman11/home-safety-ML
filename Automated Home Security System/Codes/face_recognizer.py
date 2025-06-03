import cv2
import numpy as np
import json
import os
import time
from datetime import datetime

if __name__ == "__main__":
    # Create and load the LBPH face recognizer model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer.yml')  # Load the trained recognizer model
    
    # Load Haar cascade for face detection
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Load user names from the 'names.json' file
    with open('names.json', 'r') as fs:
        names = list(json.load(fs).values())  # Convert names to a list

    # Open the webcam
    cam = cv2.VideoCapture(0)  # Use default webcam
    if not cam.isOpened():  # Check if the camera feed is opened successfully
        print("[ERROR] Could not open webcam.")
        exit()

    cam.set(3, 640)  # Set width of the video frame
    cam.set(4, 480)  # Set height of the video frame
    minW, minH = 0.1 * cam.get(3), 0.1 * cam.get(4)  # Set minimum face size as 10% of frame

    # Prepare directory to store images of intruders
    intruder_dir = "intruder_images"  # Directory name
    os.makedirs(intruder_dir, exist_ok=True)  # Create directory if it doesn't exist

    while True:  # Loop to continuously capture frames from the camera
        ret, img = cam.read()  # Read a frame from the camera
        if not ret:  # Check if the frame was captured successfully
            print("[ERROR] Failed to capture frame.")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale

        # Detect faces in the frame
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))

        face_recognized = False  # Track if a known face is detected
        
        for (x, y, w, h) in faces:  # Process each detected face
            # Predict the face ID and confidence level
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if confidence < 75 and id < len(names):  # If confidence is high and ID is valid
                name = names[id]  # Get the name for the recognized ID
                confidence_text = f"  {100 - round(confidence)}%"  # Confidence as percentage
                face_recognized = True  # Mark face as recognized
            else:  # If face is not recognized
                name = "Unknown"  # Mark face as unknown
                confidence_text = "N/A"  # No confidence value
                
                # Save the intruder's image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Generate timestamp
                intruder_image_path = os.path.join(intruder_dir, f"intruder_{timestamp}.jpg")  # File path
                cv2.imwrite(intruder_image_path, img)  # Save the intruder's image
                print(f"Intruder detected, image saved at {intruder_image_path}")  # Log intruder detection

            # Draw a rectangle around the face
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Display the name of the person
            cv2.putText(img, name, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            # Display the confidence level
            cv2.putText(img, confidence_text, (x + 5, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)  # Show the video feed with annotations

        if cv2.waitKey(10) & 0xff == 27:  # Exit the loop if 'Escape' key is pressed
            break

    # Cleanup
    cam.release()  # Release the camera
    cv2.destroyAllWindows()  # Close all OpenCV windows
