import numpy as np
import argparse
import cv2

##Will detect the circle in the image
## can get an output of the center and radius of the circle
filename = "test.tiff"
path = f"C:/Users/nxrni/Documents/Nicholas School/nicholas school/Sophmore/light pollution/image analysis/original photos/{filename}"

image = cv2.imread(path)
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
## variables in HoughCircles can be adjusted to get results, the 1.2, 100 with min and Max Radius
## seem to work well for an example all-sky image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2,100, minRadius=400, maxRadius=1000)
# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		print (x, y, r)
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

cv2.imshow("output", np.hstack([image, output]))
cv2.waitKey(0)
