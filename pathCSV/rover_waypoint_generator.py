import cv2
import numpy

image = cv2.imread("path_image.jpg", cv2.IMREAD_GRAYSCALE)
binaryImage = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

imageHeight = binaryImage.shape[0]
imageWidth = binaryImage.shape[1]

centerX = int(imageWidth / 2)
centerY = int(imageHeight / 2)

dictDistanceSum, dictCount = dict(), dict()
dictWaypoints, dictRadius = dict(), dict()

angleKeys = numpy.linspace(-3.1, 3.1, 63)
for angleKey in angleKeys:
	dictDistanceSum[round(angleKey, 1)] = 0
	dictCount[round(angleKey, 1)] = 0

for i in range(imageWidth):
	for j in range(imageHeight):
		if binaryImage[j][i] == 255:
			thetaRound = round(numpy.arctan2((j - centerY), (i - centerX)), 1)
			distance = numpy.sqrt((j - centerY) * (j - centerY) + (i - centerX) * (i - centerX))
			dictCount[thetaRound] += 1
			dictDistanceSum[thetaRound] += distance

for angleKey in angleKeys:
	thetaRound = round(angleKey, 1)
	dictRadius[thetaRound] = dictDistanceSum[thetaRound] / dictCount[thetaRound]

	waypointX = centerX + dictRadius[thetaRound] * numpy.cos(thetaRound)
	waypointY = centerY + dictRadius[thetaRound] * numpy.sin(thetaRound)
	print(thetaRound, int(waypointX), int(waypointY))
	cv2.circle(image, (int(waypointX), int(waypointY)), 3, 127, 3)

cv2.imshow("x", image)
cv2.waitKey(0)