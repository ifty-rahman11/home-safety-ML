import cv2
import json
import os

def get_face_id(directory: str) -> int: # Function to assign each face a unique user ID
    if not os.path.exists(directory): # Check if the directory exists
        os.makedirs(directory) # Create the directory if it doesn't exist
    user_ids = {int(filename.split("-")[1]) for filename in os.listdir(directory) if filename.startswith("Users-")} # Store the user ID by splitting filename
    return next(i for i in range(len(user_ids) + 1) if i not in user_ids) # Returns the next available user ID

def save_name(face_id: int, face_name: str, filename: str) -> None: # Function to save each face with a unique ID in a JSON file
    names_json = {} # Declare dictionary to store names
    if os.path.exists(filename): # Check if the file exists
        with open(filename, 'r') as fs: # Open the file in read mode
            names_json = json.load(fs) # Load existing data
    names_json[face_id] = face_name # Assign unique ID to each face
    with open(filename, 'w') as fs: # Open the file in write mode
        json.dump(names_json, fs, ensure_ascii=False, indent=4) # Store updated dictionary to the file in a readable format

if __name__ == '__main__':
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') # Load Haar cascade classifier
    cam = cv2.VideoCapture(0) # Turn on the webcam
    if not cam.isOpened(): # Check if the webcam is opened successfully
        print("[ERROR] Could not open webcam. Please check your camera settings.")
        exit()

    cam.set(3, 640) # Set webcam frame width
    cam.set(4, 480) # Set webcam frame height

    num_people = int(input("Enter the number of people to capture images for: ")) # Ask user to input the number of people

    for _ in range(num_people):
        count, face_name = 0, input('\nEnter user name: ') # Reset count and ask for user name
        face_id = get_face_id('images') # Call get_face_id function and assign a unique ID
        save_name(face_id, face_name, 'names.json') # Save the name and ID in the JSON file
        print(f'\n[INFO] Capturing images for {face_name}...')

        while count < 30: # Capture up to 30 images
            ret, img = cam.read() # Capture a frame from the webcam
            if not ret: # Check if the frame was captured successfully
                print("[ERROR] Failed to capture image from webcam.")
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert the frame to grayscale
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100)) # Detect faces in the grayscale image

            if len(faces) == 0: # If no faces are detected
                print("[INFO] No faces detected. Adjust lighting or camera angle.")
            else:
                for (x, y, w, h) in faces: # Locate the face
                    # Ensure the detected region is a valid face
                    if w > 50 and h > 50:  # Filter out small detections
                        count += 1
                        face_roi = gray[y:y+h, x:x+w]  # Extract the face region
                        cv2.imwrite(f'./images/Users-{face_id}-{count}.jpg', face_roi) # Save the cropped grayscale image
                        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2) # Draw a rectangle around the face
                        cv2.putText(img, face_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2) # Display the name above the bounding box

            cv2.imshow('Video Feed', img) # Display the video feed with annotations

            if cv2.waitKey(100) & 0xff == 27 or count >= 30: # Press 'Esc' to exit or stop after 30 images
                break

        print(f'\n[INFO] Successfully captured images for {face_name}.')

    print('\n[INFO] Exiting Program.')
    cam.release() # Release the webcam
    cv2.destroyAllWindows() # Close all OpenCV windows