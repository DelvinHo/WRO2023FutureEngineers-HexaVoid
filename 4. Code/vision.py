from threading import Thread, Event
from queue import Queue
from picamera2 import Picamera2
import cv2 as cv
import numpy as np

"""
Steps in the computer vision file
1. Image de-noising/smoothing
2. Convert BGR to HSL for object masking
3. Object masking (Morphological Transformations if (1) and (2)'s results not good enough)
4. Optimise object mask by eroding and dilating
5. Pick the largest contour, if any
6. Get the image moment of the picked contour
7. Draw the contour and its center, along with its y-axis
8. 
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
frames_queue = Queue(maxsize=5) 


# Function to continuously read frames from the camera
def read_frames(event):
    while True:
        if event.is_set():
            break

        # in Blue-Red-Green-Alpha (BRGA) format
        frame = camera.capture_array()
        frames_queue.put(frame)


# Function to process and display frames
def process_frames(event):
    while True:
        if event.is_set():
            break

        frame = frames_queue.get()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (5, 5), 0)

        # Threshold the HSV image to get only green colors
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, (HSV_GREEN - HSV_THRESHOLD)[0][0], (HSV_GREEN + HSV_THRESHOLD)[0][0])
        mask = cv.erode(mask, None, iterations=2)
        mask = cv.dilate(mask, None, iterations=2)
        
        # Bitwise-AND mask and original image
        res = cv.bitwise_and(blurred, blurred, mask=mask)

        # thresh = cv.threshold(res, 60, 255, cv.THRESH_BINARY)
        # cnts = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # image = cv.drawContours(res, cnts, -1, (0,255,0), 3)

        # ret, thresh = cv.threshold(res, 60, 255, 0)
        # thresh = cv.adaptiveThreshold(res, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

        ret, thresh =  cv.threshold(res, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # only proceed if at least one contour was found
        if len(contours) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(contours, key=cv.contourArea)
            # ((x, y), radius) = cv.minEnclosingCircle(c)
            # compute the center of the contour
            M = cv.moments(c)
            
            if M["m00"] != 0: 
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
                # draw the contour and center of the shape on the image
                cv.drawContours(res, [c], -1, (0, 255, 0), 2)
                cv.circle(res, center, 7, (255, 0, 0), -1)

        # height, width = res.shape
        # min_x, min_y = width, height
        # max_x = max_y = 0

        # # computes the bounding box for the contour, and draws it on the frame,
        # for contour in contours:
        #     global output
        #     (x, y, w, h) = cv.boundingRect(contour)
        #     min_x, max_x = min(x, min_x), max(x + w, max_x)
        #     min_y, max_y = min(y, min_y), max(y + h, max_y)

        #     if w > 80 and h > 80:
        #         output = cv.rectangle(res, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # if max_x - min_x > 0 and max_y - min_y > 0:
        #     output = cv.rectangle(res, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)


        # # output = cv.drawContours(res, contours, -1, (255, 0, 0), 3)

        # cv.imshow('Contours', output)
        cv.imshow('Masked green', res)
        cv.imshow('Original', blurred)
        
        # if the 'q' key is pressed, stop the loop
        key = cv.waitKey(1) & 0xFF
        if key == ord("q"):
            event.set()
            break


event = Event()

# Create threads
read_thread = Thread(target=read_frames, args=(event,))
process_thread = Thread(target=process_frames, args=(event,))

# Start threads
read_thread.start()
process_thread.start()

# Wait for threads to finish
read_thread.join()
process_thread.join()
camera.close()

print("Stopping")
cv.destoryAllWindows()