import cv2
import numpy as np
from PIL import Image
import os
if __name__ == "__main__":
    path = './images/' #Image directory
    recognizer = cv2.face.LBPHFaceRecognizer_create() #Creates a Local Binary Patterns Histograms (LBPH) face recognizer, used for face recognition and training.
    print("\n[INFO] Training...")
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') #Loads Haarcascade model
    def getImagesAndLabels(path): #Defines a function to load face images and their corresponding labels (IDs).
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)] #Collects all image file paths in the specified directory.
        #Prepares empty lists to store face data and corresponding IDs
        faceSamples = []
        ids = []
        for imagePath in imagePaths: #Iterates over each image in the directory.
            PIL_img = Image.open(imagePath).convert('L') #Covert to grayscale image
            img_numpy = np.array(PIL_img, 'uint8') #Convert image to numoy array
            id = int(os.path.split(imagePath)[-1].split("-")[1])# Extract the user ID from the image file name
            faces = detector.detectMultiScale(img_numpy)# Detect faces in the grayscale image
            for (x, y, w, h) in faces: #Locates the faces in the frame
                faceSamples.append(img_numpy[y:y+h, x:x+w]) # Extract face region and append to the samples
                ids.append(id) #Adds the user ID to the ids list.
        return faceSamples, ids 
    faces, ids = getImagesAndLabels(path)
    # Train the recognizer with the face samples and corresponding labels
    recognizer.train(faces, np.array(ids))
    # Save the trained model into the current directory
    recognizer.write('trainer.yml')
    print("\n[INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
