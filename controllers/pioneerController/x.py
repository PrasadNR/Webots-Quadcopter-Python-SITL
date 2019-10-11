import cv2
from cv2 import aruco

grayImage = cv2.imread("D:\\STATUS\\protos\\textures\\Aruco.png", 0)
image = cv2.imread("D:\\STATUS\\protos\\textures\\Aruco.png")

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL) 
result = cv2.aruco.detectMarkers(grayImage, dictionary)

x1 = result[0]
for i, c in enumerate(x1[0][0]):
	cv2.circle(image, (int(c[0]), int(c[1])), 2, (0,255,0), 3)

cv2.imshow("aruco", image)
cv2.waitKey(0)