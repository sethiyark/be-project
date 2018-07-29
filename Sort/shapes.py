import cv2
import imutils

from PixelRatio import get_pixel_per_metric


class ShapeDetector:
    def __init__(self):
        pass

    @staticmethod
    def detect(c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"
        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            shape = "square" if 0.95 <= ar <= 1.05 else "rectangle"

        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"

        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"

        # return the name of the shape
        return shape


ppm = get_pixel_per_metric('ref.png', 100)
cap = cv2.VideoCapture(1)

ret, image = cap.read()

# image = cv2.imread('capture.png')
# resized = imutils.resize(image, width=300)
# ratio = image.shape[0] / float(resized.shape[0])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
# img = cv2.medianBlur(gray, 5)
# ret, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)
img = cv2.Canny(gray, 0, 255)
img = cv2.dilate(img, None, iterations=1)
img = cv2.erode(img, None, iterations=1)
# print thresh

# convert the resized image to grayscale, blur it slightly,
# and threshold it
# gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()

result = {}

# loop over the contours
for c in cnts:
    if cv2.contourArea(c) < 100:
        continue
    elif cv2.contourArea(c) > 100000:
        continue
    else:
        ((cX, cY), radius) = cv2.minEnclosingCircle(c)

        shape = sd.detect(c)
        result[shape] = [cX / ppm, cY / ppm]

        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        c = c.astype("float")
        c = c.astype("int")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2)

        cv2.imshow("Image", image)
        # cv2.imshow("Thresh", img)

cv2.waitKey(0)
print
result
