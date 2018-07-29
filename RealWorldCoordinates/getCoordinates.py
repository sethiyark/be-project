import cv2
import imutils
from PixelRatio import get_pixel_per_metric
from angle import get_angle
from imutils import contours
from mdi import *

mdi_conn = MDI()
telnet_connect(mdi_conn)

ppm = get_pixel_per_metric("ref.png", 100)
cord = []

target_velocity = 10
destination = [300, 400, 30]
wait_pos = [150, 250, 200]

go(mdi_conn, wait_pos[0], wait_pos[1], wait_pos[2])
cap = cv2.VideoCapture(1)

while True:
    try:
        ret, frame = cap.read()
        # frame = cv2.imread("capture.png")
        # Our operations on the frame come here

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        # img = cv2.medianBlur(gray, 5)
        # ret, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)
        img = cv2.Canny(gray, 0, 255)
        img = cv2.dilate(img, None, iterations=1)
        img = cv2.erode(img, None, iterations=1)
        # print thresh

        # find the contours in the mask, then sort them from left to right
        # Descriptors of the objects
        cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        if len(cnts) > 0:
            cnts = contours.sort_contours(cnts)[0]
            # loop over the contours
            for (i, c) in enumerate(cnts):
                # draw the bright spot on the image
                if cv2.contourArea(c) < 1000:
                    continue
                elif cv2.contourArea(c) > 100000:
                    continue
                else:
                    ((cX, cY), radius) = cv2.minEnclosingCircle(c)
                    cord.append([cX / ppm, cY / ppm, get_angle(frame)])
                    # print(str(cX) + " " + str(cY))
        # print(len(cnts))
        # cv2.imshow("frame", frame)
        # cv2.imshow("gray", gray)
        # cv2.waitKey(0)
        ht, wd, c = frame.shape
        print(cord)
        if cord[-1]:
            go(mdi_conn, cord[0][0], cord[0][1] + (target_velocity * 1), 10)
            time.sleep(3)
            go(mdi_conn, cord[0][0], cord[0][1] + (target_velocity * 3))
            time.sleep(0.1)
            # Pick
            go(mdi_conn, wait_pos[0], wait_pos[1], wait_pos[2])
            time.sleep(0.05)
            go(mdi_conn, destination[0], destination[1], destination[2] + 10)
            time.sleep(0.1)
            go(mdi_conn, destination[0], destination[1], destination[2] + 5)
            time.sleep(0.25)
            # Place
            go(mdi_conn, destination[0], destination[1], destination[2])
            go(mdi_conn, wait_pos[0], wait_pos[1], wait_pos[2])
            cord = []
    except:
        continue

# cv2.imshow("edge", img)


#    while True:
#        if cv2.waitKey(0) & 0xFF == ord('q'):
#            break
# cv2.imshow("thresh", thresh)
# Check to Terminate


cv2.destroyAllWindows()
