import cv2
import numpy as np


def get_angle(frame):
    # Our operations on the frame come here
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 80)
    angle = 0
    if lines is not None and len(lines) == 1:
        for rho, theta in lines[0]:
            angle = 90 - (theta * 180 / np.pi)
            if angle < 0:
                angle += 180
    elif lines is not None and len(lines) > 1:
        theta_i = None
        for l in lines:
            for rho, theta in l:
                if theta_i is None:
                    theta_i = theta
                if (theta_i - theta) <= 0.05 * theta_i:
                    continue

        for rho, theta in lines[0]:
            angle = 90 - (theta * 180 / np.pi)
            if angle < 0:
                angle += 180

    return angle
