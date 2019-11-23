import cv2
import csv

global clickCoordinates
clickCoordinates = list()

def click_point(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		clickCoordinates.append((x, y))

image = cv2.imread("rover_circuit.jpg")
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_point)

while True:
	cv2.imshow("image", image)
	key = cv2.waitKey(1)
	if key == ord(" "):
		break

with open('waypoints.csv', 'w', newline='') as f:
	writer = csv.writer(f)
	writer.writerow(["waypointID", "coordinateX", "coordinateY"])
	for coordinateID, eachClickCoordinatePair in enumerate(clickCoordinates):
		writer.writerow([coordinateID, eachClickCoordinatePair[0], eachClickCoordinatePair[1]])