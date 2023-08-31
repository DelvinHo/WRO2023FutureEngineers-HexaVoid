import threading
import queue
import numpy as np
import cv2 as cv


"""
Steps in the computer vision file
(Current) 1. Image de-noising/smoothing
2. 
"""

# Function to continuously read frames from the camera
def read_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frames_queue.put(frame)

# Function to process and display frames
def process_frames():
    while True:
        frame = frames_queue.get()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera or camera not found")

# Queue to hold frames
frames_queue = queue.Queue(maxsize=5)  # Set an appropriate size

# Create threads
read_thread = threading.Thread(target=read_frames)
process_thread = threading.Thread(target=process_frames)

# Start threads
read_thread.start()
process_thread.start()

# Wait for threads to finish
read_thread.join()
process_thread.join()

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
