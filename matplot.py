import numpy as np
from PIL import Image
import matplotlib as mp
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from tifffile import imread, imshow


## Shows the original image unaltered
def show_image(filename):
    filepath = f"C:/Users/nxrni/Documents/Nicholas School/nicholas school/Sophmore/light pollution/image analysis/original photos/{filename}"
    image = Image.open(filepath)
    image = image.convert('L')
    array = np.array(image)
    new_image = Image.fromarray(array)
    new_image.show()
    
## Creating an intensity contour plot for an image
## Input: filename a file in the form "filename.jpg"
## The image file can be colored or grayscaled
## Output: The contour path
def contour(filename): ## I.e "filename.jpg"
    filepath = f"C:/Users/nxrni/Documents/Nicholas School/nicholas school/Sophmore/light pollution/image analysis/original photos/{filename}"

    image = Image.open(filepath)
    image = image.convert('L')
    array = np.array(image)
    #print(array)
    x = 0## x coordinate of pixel
    y = 0## y coordinate of pixel
    print (array[x,y])
    shape = array.shape ## Tuple of (xmax, ymax)
    print (shape)
    xmax = shape[0]
    ymax = shape[1]

    ## Trying to plot
    fig, ax = plt.subplots()
    #ax.contour(array)
    cont_set = ax.contourf(array, cmap='magma')
    #ax.clabel(cont_set, inline=True, fontsize=10)
    ax.set_title("testing")
    plt.show()

##Plots the average intensity for radial distance from zenith
def rad_int(filename):
    filepath = f"C:/Users/nxrni/Documents/Nicholas School/nicholas school/Sophmore/light pollution/image analysis/original photos/{filename}"
    image = imread(filepath)
    imshow(image)
    plt.show()
    xmax = image.shape[0]
    ymax = image.shape[1]
    #Zenith
    cen_x = xmax//2
    cen_y = ymax//2
    print(cen_x, cen_y)
    #Find radial distance
    [X,Y] = np.meshgrid(np.arange(ymax)-cen_x, np.arange(xmax)-cen_y)
    R = np.sqrt(np.square(X)+np.square(Y))
    rad = np.arange(1, np.max(R), 1)
    intensity = np.zeros(len(rad))
    index = 0
    bin_size = 1 ## how many pixels each radius differs
    for i in rad:
        mask = (np.greater(R, i - bin_size) & np.less(R, i +bin_size))
        values = image[mask]
        intensity[index]= np.mean(values)
        index +=1
    # Adjust plot parameters
    mp.rcParams['font.family'] = 'Avenir'
    mp.rcParams['font.size'] = 16
    mp.rcParams['axes.linewidth'] = 2
    mp.rcParams['axes.spines.top'] = False
    mp.rcParams['axes.spines.right'] = False
    mp.rcParams['xtick.major.size'] = 7
    mp.rcParams['xtick.major.width'] = 2
    mp.rcParams['ytick.major.size'] = 7
    mp.rcParams['ytick.major.width'] = 2
    #create figures
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(rad, intensity, linewidth=2)
    ax.set_xlabel('Radial Distance',labelpad=10)
    ax.set_ylabel('Average Intensity', labelpad=10)
    
        
