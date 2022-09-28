# perception-challenge-solution
Wisconsin Autonomous perception coding challenge 

## Methodology
Using OpenCV I first converted the image to HSV and used the inRange function with the HSV threshold of the cone to single out the cones. Next dilate and canny was added to the image to make the cones more visible. Then contours were found and each object was checked to see if it was big enough to be a cone using a rectangle surrounding the object. If it was big enough it was added the coordinate of the cone to the corresponding line array. Finally, using these coordinates a line of best fit is found and drawn onto the image.

## What did you try and why do you think it did not work.
I first tried to just find all the contours on the image and see which ones were cone shaped. This way was unecessarily long and hard because of the amount of edges it detected on the image and the difficulty of seeing which ones were cone shaped. Another problem I came across were the additional bits of noise that the threshold couldn't get rid of. There were just some objects of similar color to the cone. I solved this by checking if the bounding rectangle was of a large enough size to be a cone. 

## What libraries are used
opencv / numpy

![answer](https://github.com/jerluo/perception-challenge-solution/blob/main/answer.png?raw=true)
