from controller import *
import roverHelper
import cv2
import numpy as np

TIME_STEP = 64

robot = Robot()

[frontLeftMotor, frontRightMotor, backLeftMotor, backRightMotor] = roverHelper.getMotorAll(robot)
MAX_WHEEL_VELOCITY = frontLeftMotor.getMaxVelocity()

timestep = int(robot.getBasicTimeStep())
roverHelper.initialiseMotors(robot, MAX_WHEEL_VELOCITY)

gps = GPS("gps")
gps.enable(TIME_STEP)

camera = Camera("camera")
camera.enable(TIME_STEP)

teleoperaton = False #THIS IS ONLY FOR DEBUGGING PURPOSES AND USAGE IN PRODUCTION IS HIGHLY DISCOURAGED. SET THIS TO False WHEN ROVER HAS TO BE AUTONOMOUS.

if teleoperaton == True:
	keyboard = Keyboard();
	keyboard.enable(TIME_STEP);
	cv2.startWindowThread()
	cv2.namedWindow("centroid")

while (robot.step(timestep) != -1):

	if teleoperaton == True:
		key = keyboard.getKey();
		if key == keyboard.UP:
			roverHelper.movement.forward(robot, MAX_WHEEL_VELOCITY)
		if key == keyboard.LEFT:
			roverHelper.movement.left(robot, MAX_WHEEL_VELOCITY)
		if key == keyboard.DOWN:
			roverHelper.movement.backward(robot, MAX_WHEEL_VELOCITY)
		if key == keyboard.RIGHT:
			roverHelper.movement.right(robot, MAX_WHEEL_VELOCITY)
		if key == keyboard.END:
			roverHelper.movement.brake(robot, MAX_WHEEL_VELOCITY)

	gpsLocation = gps.getValues()
	cameraData = camera.getImage()
	image = np.frombuffer(cameraData, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4)) #BGRA
	
	red = image[int(camera.getHeight()/2):camera.getHeight(), :, 2]
	green = image[int(camera.getHeight()/2):camera.getHeight(), :, 1]
	blue = image[int(camera.getHeight()/2):camera.getHeight(), :, 0]

	hsvImage = cv2.cvtColor(np.dstack((blue, green, red)), cv2.COLOR_BGR2HSV)
	lowerHSV = np.array([120, 0, 50])
	upperHSV = np.array([180, 255, 200])

	momentMask = cv2.inRange(hsvImage, lowerHSV, upperHSV)
	moment = cv2.moments(momentMask, False)
	
	try:
		cX = int(moment["m10"] / moment["m00"])
		cY = int(moment["m01"] / moment["m00"])
	except ZeroDivisionError:
		cX, cY = int(camera.getHeight()/2), int(camera.getWidth()/2)

	k = (2 * cX - camera.getWidth()) / camera.getWidth()
	roverHelper.lineFollow(robot, MAX_WHEEL_VELOCITY, k)

	if teleoperaton == True:
		cXdisplay, cYdisplay = int(cX), int(cY + camera.getHeight()/2)
		cv2.circle(image, (cXdisplay, cYdisplay), 2, (0,255,0), 3)
		cv2.imshow("centroid", image)
		cv2.waitKey(TIME_STEP)