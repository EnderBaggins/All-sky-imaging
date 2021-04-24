import numpy as np
from PIL import Image, ImageDraw, ImageShow
import matplotlib as mp
import matplotlib.pyplot as plt
from tifffile import imread, imshow
import cv2

'''##Accessing filepath for lab's computer
## Input filename
## output the filepath
def path(filename):
    path = f"/Users/gokhale/Desktop/Python Image Processing/photo_work/original_images/{filename}"
    return path
'''
##Accessing filepath for personal computer
## Input filename
## output the filepath
def path(filename):
    path = f"C:/Users/nxrni/Documents/Nicholas School/nicholas school/Sophmore/light pollution/image analysis/original photos/{filename}"
    return path

## finding the center and radius of the all-sky image
## Input: image (a numpy array of an image)
## Output: a three-tuple of xcen, ycen, radius
def find_center(image):
    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ## variables in HoughCircles can be adjusted to get results, the 1.2, 100 with min and Max Radius
    ## seem to work well for an example all-sky image
    ## the variables there depend highly on the size of the all-sky image
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2,100, minRadius=400, maxRadius=1000)
    # ensure at least some circles were found
    if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            ## for all-sky image it should only have 1 set
            for (x, y, r) in circles:
                    r = int(r)
                    ##prints the appropriate (x,y, radius values)
                    return (x, y, r)

##Cropping out the smallest square surrounding all-sky image
## Calls the find_center function to find center and radius
def crop(filename):
    filepath = path(filename)
    image = cv2.imread(filepath)
    x,y,radius = find_center(image)
    x0, x1 = x-radius, x+radius
    y0,y1 = y-radius, y+radius
    cropped_image = image[y0:y1,x0:x1]
    #imshow(cropped_image)
    #plt.show()
    return (cropped_image, radius)
##Creates a contour image of the tiff file
def contour(filename):
    ##The cropping of image is not entirely necessary
    image, radius = crop(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    fig, ax = plt.subplots()
    cont_set = ax.contourf(image, cmap='magma')
    ax.set_title("Contour plot")
    plt.show()
