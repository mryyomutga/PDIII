import numpy as np
import cv2

img = np.full((500, 500, 3), 64, dtype=np.uint8)
point = [[50, 200], [150, 200], [150, 100]]
pts = np.array(point, np.int32)
pts = pts.reshape((-1, 1, 2))

img = cv2.fillPoly(img, [pts], (16, 128, 255))

cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
