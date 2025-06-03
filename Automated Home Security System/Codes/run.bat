@echo off
python face_taker.py 
python face_train.py 
python face_recognizer.py
start /B python mail.py
python fireDetection.py




