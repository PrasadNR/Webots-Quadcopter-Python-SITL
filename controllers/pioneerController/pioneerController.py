from controller import *
import roverHelper
import cv2
import numpy
import csv

params = dict()
with open("../params.csv", "r") as f:
	lines = csv.reader(f)
	for line in lines:
		params[line[2]] = line[3]

TIME_STEP = int(params["ROVER_TIME_STEP"])

robot = Robot()

[frontLeftMotor, frontRightMotor, backLeftMotor, backRightMotor] = roverHelper.getMotorAll(robot)
MAX_WHEEL_VELOCITY = frontLeftMotor.getMaxVelocity()

timestep = int(robot.getBasicTimeStep())
roverHelper.initialiseMotors(robot, MAX_WHEEL_VELOCITY)

gps = GPS("gps")
gps.enable(TIME_STEP)

camera = Camera("camera")
camera.enable(TIME_STEP)

emitter = Emitter("emitter")

teleoperaton = False #THIS VARIABLE IS ONLY FOR DEBUGGING PURPOSES AND USAGE OF THIS VARIABLE IN PRODUCTION IS HIGHLY DISCOURAGED. SET THIS TO False WHEN ROVER HAS TO BE AUTONOMOUS.

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
	image = numpy.frombuffer(cameraData, numpy.uint8).reshape((camera.getHeight(), camera.getWidth(), 4)) #BGRA

	xRover, yRover = gps.getValues()[2], gps.getValues()[0]
	emitter.send((str(xRover) + ", " + str(yRover)).encode('utf-8'))
	
	red = image[int(camera.getHeight()/2):camera.getHeight(), :, 2]
	green = image[int(camera.getHeight()/2):camera.getHeight(), :, 1]
	blue = image[int(camera.getHeight()/2):camera.getHeight(), :, 0]

	hsvImage = cv2.cvtColor(numpy.dstack((blue, green, red)), cv2.COLOR_BGR2HSV)
	lowerHSV = numpy.array([int(params["low_H"]), int(params["low_S"]), int(params["low_V"])])
	upperHSV = numpy.array([int(params["high_H"]), int(params["high_S"]), int(params["high_V"])])

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
		cv2.circle(image, (cXdisplay, cYdisplay), int(params["display_dot_radius"]), (int(params["display_dot_R"]), int(params["display_dot_G"]), int(params["display_dot_B"])), int(params["display_dot_thickness"]))
		cv2.imshow("centroid", image)
		cv2.waitKey(TIME_STEP)