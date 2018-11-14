import numpy as np
import cv2

r = 100
arg = np.radians([-180,-150,-135,-120,-90,-60,-45,-30,0,30,45,60,90,120,135,150,180])
img = np.full((400,400,3), 64, dtype=np.uint8)

points = [[0,0] for i in range(len(arg))]
for i, rad in enumerate(arg):
    points[i][0] = int(r * np.cos(rad)) + 200
    points[i][1] = int(r * np.sin(rad)) + 200

for i, p in enumerate(points):
    if i == len(arg) - 1:
        i = 0
    pts = [[200,200], p, points[i + 1]]
    tri = np.array(pts, np.int32)
    tri = tri.reshape((-1, 1, 2))
    img = cv2.fillPoly(img, [tri], (255, 255, 255))
    img = cv2.line(img, (p[0], p[1]), (points[i][0], points[i][1]), (0,0,0))

cv2.imshow("test cv map", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
