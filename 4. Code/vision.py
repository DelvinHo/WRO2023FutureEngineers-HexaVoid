import time
import threading
import queue
from picamera2 import Picamera2
import cv2 as cv
import numpy as np

"""
Steps in the computer vision file
1. Image de-noising/smoothing
2. Convert BGR to HSL for object masking
3. Object masking
"""

# The colour of the red traffic signs is RGB (238, 39, 55).
# The colour of the green traffic signs is RGB (68, 214, 44).

KERNEL = np.ones((5,5),np.float32) / 25
HSV_RED = cv.cvtColor(np.uint8([[[55, 39, 238]]]), cv.COLOR_BGR2HSV)
HSV_GREEN = cv.cvtColor(np.uint8([[[44, 214, 68]]]), cv.COLOR_BGR2HSV)
HSV_THRESHOLD = 30

# Initialize the camera
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888'}))
camera.start()

# Queue to hold frames
frames_queue = queue.Queue(maxsize=5) 


# Function to continuously read frames from the camera
def read_frames():
    while True:
        # in Blue-Red-Green-Alpha (BRGA) format
        frame = camera.capture_array()
        frames_queue.put(frame)


# Function to process and display frames
def process_frames():
    while True:
        smoothed = frames_queue.get()

        #smoothed = cv.blur(frame,(10,10))
        #smoothed = cv.filter2D(frame, -1, KERNEL)

        # Threshold the HSV image to get only blue colors
        hsv = cv.cvtColor(smoothed, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, (HSV_GREEN - HSV_THRESHOLD)[0][0], (HSV_GREEN + HSV_THRESHOLD)[0][0])
        
        # Bitwise-AND mask and original image
        res = cv.bitwise_and(smoothed, smoothed, mask= mask)

        cv.imshow('Masked green', res)
        cv.imshow('Original', smoothed)
        
        if cv.waitKey(1) == ord('q'):
            break


# Create threads
read_thread = threading.Thread(target=read_frames)
process_thread = threading.Thread(target=process_frames)

# Start threads
read_thread.start()
process_thread.start()

# Wait for threads to finish
read_thread.join()
process_thread.join()
camera.close()