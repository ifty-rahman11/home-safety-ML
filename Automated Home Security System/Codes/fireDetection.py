import cv2  # Library for OpenCV
import pygame #for playing the siren sound
pygame.mixer.init() #to initialize the pygame mixer

siren_sound = r"C:\Users\VICTUS\OneDrive\Desktop\Fifth Semester\Courses\LABS\EEE-4518\Project\Files\Automated Home Security System\Codes\siren-alert-96052.wav"
fire_cascade = cv2.CascadeClassifier(r"C:\Users\VICTUS\OneDrive\Desktop\Fifth Semester\Courses\LABS\EEE-4518\Project\Files\Automated Home Security System\Codes\fire_detection_cascade_model.xml") #Haar Cascade model file

vid = cv2.VideoCapture(0) #opening the webcam of laptop

while True:
    ret, frame = vid.read() #read each frame from the video
    if not ret:
        break  # loop will continue until frame is captured properly

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converting to Grayscale (Black & White) to improve accuracy
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) #detecting fire-like patterns in the frame. here frame indicates the input image, 1.2 indicates how much the image size is reduced at each scale, 5 is the minimum number of neighbors

    if len(fire) > 0:
        pygame.mixer.music.load(siren_sound)  # if fire is found, siren sound will be played
        pygame.mixer.music.play() 
    
    for (x, y, w, h) in fire: #(x,y) indicates top-left corner of detected fire, w indicates width & h indicates height of the detected fire region
        cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 0, 255), 2) #drawing a rectangle around the area where fire is detected
        print("Fire detected!") 
    
    cv2.imshow('Fire Detection', frame) #displays video frame with detected fire in openCV window

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:  #pressing 'q' or 'Esc' from keyboard will terminate the program
        break

vid.release() #stop the webcam
cv2.destroyAllWindows() #close all openCV windows
pygame.mixer.quit() #shut down the pygame module