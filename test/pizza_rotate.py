import cv2
import numpy as np
import time
cv2.namedWindow('demo', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
cv2.resizeWindow('demo', 700,700)

image = np.ones((700, 700, 3), np.uint8)*100

deg=np.random.randint(0,360)
pt1=(np.random.randint(300,400),np.random.randint(300,400)) # 回転の中心
while True:
    deg %=360
    dist=np.random.randint(20,200)
    pt2 = (int(dist*np.cos(deg/180*np.pi)+pt1[0]), int(dist*np.sin(deg/180*np.pi)+pt1[1]))
    deg+=10
    pt3 =  (int(dist*np.cos(deg/180*np.pi)+pt1[0]), int(dist*np.sin(deg/180*np.pi)+pt1[1]))
    
    cv2.circle(image, pt1, 10, (255,255,255), -1)
    triangle_cnt = np.array( [pt1, pt2, pt3] )

    print(triangle_cnt, type(triangle_cnt[0][0]))
    cv2.drawContours(image, [triangle_cnt], 0, (0,0,0), -1)
    cv2.drawContours(image, [triangle_cnt], 0, (30,30,30), 2)

    cv2.imshow('demo', image)
    cv2.waitKey(1)

cv2.destroyAllWindows()
for _ in range (5):
    cv2.waitKey(1)
