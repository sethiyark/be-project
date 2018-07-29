import time

import cv2
from FindImpurities import scan_impurities

Tm = 1.0
Tf = 3.0
Vf = 100.0

impurities, h, w = scan_impurities()

for i in range(0, len(impurities)):
    impurities[i][0] = impurities[i][0] / w * 300
    impurities[i][1] = impurities[i][1] / h * 300

print
impurities
impurities = sorted(impurities, key=lambda x: x[1])
print
impurities
i = 1
if len(impurities) > Tf / Tm:
    print
    "can't catch them all"

else:
    for (x, y) in impurities:
        Yi = i * Tm * Vf
        print(str(x) + " " + str(Yi))
        # call to x, Yi
        time.sleep(Tm)
        # Suck

        i += 1

cv2.waitKey(0)
cv2.destroyAllWindows()
