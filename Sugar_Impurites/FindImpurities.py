import cv2
import imutils
from imutils import contours

'''
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()
cv2.imshow("frame", frame)
coordinates = []
'''


def scan_impurities():
    cord = []
    # Capture frame
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    cap.release()
    # Our operations on the frame come here
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    # img = cv2.medianBlur(gray, 5)
    # ret, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)
    img = cv2.Canny(gray, 0, 255)
    img = cv2.dilate(img, None, iterations=1)
    img = cv2.erode(img, None, iterations=1)
    # print thresh

    # find the contours in the mask, then sort them from left to
    # right

    cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    if len(cnts) > 0:
        cnts = contours.sort_contours(cnts)[0]
        # loop over the contours
        for (i, c) in enumerate(cnts):
            # draw the bright spot on the image
            if cv2.contourArea(c) < 30:
                ((cX, cY), radius) = cv2.minEnclosingCircle(c)
                cord.append([cX, cY])
                # print(str(cX) + " " + str(cY))
    # print(len(cnts))
    # cv2.imshow("frame", frame)
    # cv2.imshow("gray", gray)
    cv2.imshow("edge", img)
    # cv2.imshow("thresh", thresh)
    # Check to Terminate

    ht, wd, c = frame.shape
    return cord, ht, wd


'''
while True:
    wKey = cv2.waitKey(0) & 0xFF
    if wKey == ord('c'):
        coordinates = scan_impurities()
        print coordinates

    elif wKey == ord('q'):
        break

# When everything done, release the capture
cv2.destroyAllWindows()
'''
