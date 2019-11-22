import cv2

global clickCoordinates
clickCoordinates = list()

def click_and_crop(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		clickCoordinates.append((x, y))

image = cv2.imread("rover_circuit.jpg")
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

while True:
	cv2.imshow("image", image)
	key = cv2.waitKey(1)
	if key == ord(" "):
		break

print(clickCoordinates)