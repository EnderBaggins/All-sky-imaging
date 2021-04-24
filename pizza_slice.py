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

## Draws pizza slices on a square image of given pixel size
## input the radius of the circle and the number of sectors
## returns a list of numpy arrays of pizza slices
def slices(radius, sectors):
    angle = 360/sectors
    masks = []
    startangle = 0
    for i in range(sectors):
        image = Image.new("RGB",(2*radius,2*radius))
        draw = ImageDraw.Draw(image)
        #print(startangle)
        draw.pieslice([0,0,2*radius,2*radius], start = startangle, end = startangle+angle, fill = (255,255,255))   
        new_image = np.array(image)
        masks.append((new_image, startangle))
        startangle += angle
    return masks          

## returns the average pixel intensity of a number of pie slices from all-sky image
## in the form (ave_int, angle)
def pizza_int(filename, sectors):
    image, radius = crop(filename)
    mask_list = slices(radius, sectors)
    pie_int = []
    for i in mask_list:
        mask, angle = i
        locs = np.where(mask == 255)
        pixels = image[locs]
        ave_int = np.mean(pixels)
        ave_int = round(ave_int)
        pie_int.append((angle, ave_int))
    return pie_int
#Plots the intensity vs angle from x-axis graph
## I chose 360 sectors to be carried through automatically
## That is deltax is one degree
def pie_plot(filename):
    points = pizza_int(filename, 360)
    x = [x[0] for x in points]
    y = [y[1] for y in points]
    plt.plot(x,y)
    plt.title('directional intensity')
    plt.xlabel('angle from x-axis clockwise')
    plt.ylabel('intensity')
    plt.show()
##Plots the Average Circular Intensity vs Radial Distance
## that is it shows how sky brightness depends on how close to zenith it is
def rad_int(filename):
    image, radius = crop(filename)
    #recording size of image
    xmax = ymax = 2 * radius
    cen_x = cen_y = radius
    [X,Y] = np.meshgrid(np.arange(ymax)-cen_x, np.arange(xmax)-cen_y)
    R = np.sqrt(np.square(X)+np.square(Y))
    rad = np.arange(1,radius,1)
    intensity = np.zeros(len(rad))
    index = 0
    bin_size = 1 ## how many pixels each radius differs
    for i in rad:
        mask = (np.greater(R, i - bin_size) & np.less(R, i +bin_size))
        values = image[mask]
        #values = ma.masked_less(values, 10)## Testing Masking it works, but obviously messes up averages
        intensity[index]= np.mean(values)
        index +=1
    #create figures
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(rad, intensity, linewidth=2)
    plt.title('Radial Intensity')
    ax.set_xlabel('Radial Distance',labelpad=10)
    ax.set_ylabel('Average Intensity', labelpad=10)
    plt.show()
## Creates images from all-sky tiff file where all that is not black is a pie slice
def pizza(filename, sectors):
    #Cropping
    image,radius = crop(filename)
    mask_list = slices(radius,sectors)
    mask_list = mask_list[0]
    imagepie = []
    for mask in mask_list:
        new_image = image
        result = cv2.bitwise_and(new_image, mask)
        imagepie.append(result)
    for i in imagepie:
        #i.show()
        cv2.imshow('',i)
        cv2.waitKey()
    

