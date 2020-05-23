from __future__ import division
import cv2
import numpy as np


def nothing(*arg):
    pass

# Set the starting position of the Colour Sliders to the default red HSV range.
starting_colour = (0, 100, 80, 10, 255, 255)   # Low HSV values, followed by the High HSV values

cv2.namedWindow('HSV_Segmentation')

# Low Boundary range of the HSV Colour Sliders.
cv2.createTrackbar('Hue_Low', 'HSV_Segmentation', starting_colour[0], 255, nothing)
cv2.createTrackbar('Sat_Low', 'HSV_Segmentation', starting_colour[1], 255, nothing)
cv2.createTrackbar('Val_Low', 'HSV_Segmentation', starting_colour[2], 255, nothing)

# High Boundary range of the HSV Colour Sliders.
cv2.createTrackbar('Hue_High', 'HSV_Segmentation', starting_colour[3], 255, nothing)
cv2.createTrackbar('Sat_High', 'HSV_Segmentation', starting_colour[4], 255, nothing)
cv2.createTrackbar('Val_High', 'HSV_Segmentation', starting_colour[5], 255, nothing)

# Assign the Image file of the soccer ball to determine HSV classification.
Original = cv2.imread('red3.jpg')

# Obtain the HSV values from the Colour Sliders.
while True:
    Hue_Low = cv2.getTrackbarPos('Hue_Low', 'HSV_Segmentation')
    Sat_Low = cv2.getTrackbarPos('Sat_Low', 'HSV_Segmentation')
    Val_Low = cv2.getTrackbarPos('Val_Low', 'HSV_Segmentation')
    Hue_High = cv2.getTrackbarPos('Hue_High', 'HSV_Segmentation')
    Sat_High = cv2.getTrackbarPos('Sat_High', 'HSV_Segmentation')
    Val_High = cv2.getTrackbarPos('Val_High', 'HSV_Segmentation')

    # Display the unedited first photo that was uploaded.
    cv2.imshow('Original', Original)

    # Apply the Gaussian Blur filter to reduce unwanted noise and reduce detail to create the mask
    Image_BGR = cv2.GaussianBlur(Original, (7, 7), 0)

    # Since OpenCV is in BGR, convert the BGR from the image into the desired HSV state (model)
    hsv = cv2.cvtColor(Image_BGR, cv2.COLOR_BGR2HSV)

    # Assigning both the lowest and highest values of Hue, Saturation and Value to give the HSV range.
    Color_LowRange = np.array([Hue_Low, Sat_Low, Val_Low])
    Color_HighRange = np.array([Hue_High, Sat_High, Val_High])
    mask = cv2.inRange(hsv, Color_LowRange, Color_HighRange)

    # The getStructuring OpenCV command allows the structure of the kernel to be generated
    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

    # The Morph Close closes in small holes left in the masked image
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernal)

    # The Morph open is applied to remove noise from the background of the masked image
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)

    # Display the mask after the Morpholgical Operations have been applied
    cv2.imshow('mask', mask)

    # Inserts the mask over the original image that was uploaded
    result = cv2.bitwise_and(Original, Original, mask=mask)

    # Outputs the final image that has had the HSV model segmented
    cv2.imshow('HSV_Segmentation', result)

    # This function checks whether a key has been pressed where it then repeats the code segment
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
# Closes all windows and stops the program running
cv2.destroyAllWindows()
