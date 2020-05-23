# Import the needed packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils


# Ues the Sliders from the 'Colour Determine Package' to determine the Lower/Upper range of the HSV for the Red Ball
Red_LowerRange = (0, 145, 0)
Red_UpperRange = (19, 255, 255)

# Access the Webcam
vs = VideoStream(src=0).start()

# Perform the necessary arguments
argument_parse = argparse.ArgumentParser()
argument_parse.add_argument("-v", "--video")
argument_parse.add_argument("-b", "--buffer", type=int, default=64)
arguments = vars(argument_parse.parse_args())

# Creates a list of the tracked points from the detected ball
tracked_points = deque(maxlen=arguments["buffer"])

# Repeat the program continuously until stopped
while True:
   # grab the current frame
   currentframe = vs.read()

   # Resize the frame of the video to an appropriate size
   currentframe = imutils.resize(currentframe, width=900)

   # Apply Gaussian Blur to the image to reduce high frequency noise
   image_blurred = cv2.GaussianBlur(currentframe, (11, 11), 0)
   # image_blurred = cv2.medianBlur(currentframe, 6)
   # image_blurred = cv2.bilateralFilter(currentframe, 10,70,70)

   # Since it is in OpenCV, convert from BGR to the HSV Colour space
   hsv = cv2.cvtColor(image_blurred, cv2.COLOR_BGR2HSV)

   # Using the Upper and Lower HSV range listed from Part 1, construct the mask for the live video stream
   maskvideo = cv2.inRange(hsv, Red_LowerRange, Red_UpperRange)

   # Applying a 5x5 kernel for the morphology operations
   kernel = np.ones((5,5), np.uint8)

   # Applying the Erode Morphology removes any of the unwanted noise from the background
   maskvideo = cv2.erode(maskvideo, kernel, iterations=3)

   # Applying the Dilation Morphology adds needed pixels to the mask of the ball, filling in any unwanted gaps
   maskvideo = cv2.dilate(maskvideo, kernel, iterations=3)

   # Find the countours of the mask and designate the center point of the ball
   mask_contours = cv2.findContours(maskvideo.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   mask_contours = imutils.grab_contours(mask_contours)
   center = None

   # The program only continues if the ball has been detected, otherwise the program repeats
   if len(mask_contours) > 0:

      # Find the largest contour generated in the mask, where it will use this value to compute the outline of
      # the ball, as well as its center
      c = max(mask_contours, key=cv2.contourArea)
      ((x, y), radius) = cv2.minEnclosingCircle(c)
      M = cv2.moments(c)
      center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

      # Only proceed if the radius meets a minimum size, this removes any small speherical objects that are not the ball
      if radius > 8:

         # Outline the circumference of the ball (can change the BGR colours to select the outline colour)
         cv2.circle(currentframe, (int(x), int(y)), int(radius),(255, 255, 255), 2)

         # Highlight the center of the ball
         cv2.circle(currentframe, center, 4, (255, 0, 55), -1)

   # Refresh and update the recent tracked positions of th ball
   tracked_points.appendleft(center)


   # Reiterate the previously tracked point if the ball is stationary
   for i in range(1, len(tracked_points)):
      if tracked_points[i - 1] is None or tracked_points[i] is None:
         continue

      # Can alter the following values to change the width of the tracking line from the ball when moving
      line_width = int(np.sqrt(arguments["buffer"] / float(i + 1)) * 3.5)
      # Draw the line that connects the points of detection from the ball
      cv2.line(currentframe, tracked_points[i - 1], tracked_points[i], (255, 255, 255), line_width)

   # Output the live video stream on the window
   cv2.imshow("Frame", currentframe)

   # Output the mask generated of the ball from the live video stream on a new window
   cv2.imshow("mask", maskvideo)
   key = cv2.waitKey(1) & 0xFF

# close all windows
cv2.destroyAllWindows()
