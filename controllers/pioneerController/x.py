import cv2
from cv2 import aruco

grayImage = cv2.imread("Aruco.png", 0)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL) 
result = cv2.aruco.detectMarkers(grayImage, dictionary)

x1 = result[0]
print(x1)