import cv2 as cv
import numpy as np

def slope(array):
    #algorithm for best fit slope
    xa = 0
    ya = 0
    
    for c in array:
        xa += c[0]
        ya += c[1]
    
    xa /= len(array)
    ya /= len(array)

    top = 0
    bot = 0

    for c in array:
        xdata = (c[0]-xa)
        ydata = (c[1]-xa)

        bot += xdata * xdata
        top += xdata * ydata
    
    return top / bot

#Helper method to draw line of best fit given array of coordinates
def drawLine(image,array):

    m = slope(array)
    x1 = array[0][0]
    y1 = array[0][1]
    x2 = array[-1][0]
    y2= array[-1][1]

    h,w=image.shape[:2]
    if m!='NA':
        ### here we are essentially extending the line to x=0 and x=width
        ### and calculating the y associated with it
        ##starting point
        px=0
        py=-(x1-0)*m+y1
        ##ending point
        qx=w
        qy=-(x2-w)*m+y2
    else:
    ### if slope is zero, draw a line with x=x1 and y=0 and y=height
        px,py=x1,0
        qx,qy=x1,h
    cv.line(image, (int(px), int(py)), (int(qx), int(qy)), (0, 255, 0), 2)


img = cv.imread('red.png')

#Convert to hsv and get objects in range of the cone
hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
thres = cv.inRange(hsv, (0, 190, 149), (210, 255, 240))

#Reduce noise and create an edge
kernel = np.ones((5, 5), np.uint8)
dilation = cv.dilate(thres, kernel, iterations=1)
edged = cv.Canny(dilation,100,200)


#Find the contours
contours, hierarchy = cv.findContours(edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

#Prepping to find coordinates for each line
leftLine = []
rightLine = []

for c in contours:
    #Make sure it's actually a cone by checking it's big enough to be a cone
    M = cv.moments(c)
    area = cv.contourArea(c)
    x,y,w,h = cv.boundingRect(c)
    if w * h < 500:
        continue

    #We know it is a cone now so get points and add to array of points
    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))
    coord = (cX, cY)

    #Left line or right line
    if cX < 1000:
        if not coord in leftLine:
            leftLine.append(coord)
    else: 
        if not coord in rightLine:
            rightLine.append(coord)

#Use draw line helper method
drawLine(img, leftLine)
drawLine(img, rightLine)

cv.imwrite("answer.png", img)
cv.imshow('sample image', img)
cv.waitKey(0) # waits until a key is pressed
cv.destroyAllWindows() # destroys the window showing image
