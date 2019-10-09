from controller import *
import roverHelper
import cv2
import numpy as np

TIME_STEP = 64
MAX_WHEEL_VELOCITY = 6.4

robot = Robot()

timestep = int(robot.getBasicTimeStep())
roverHelper.initialiseMotors(robot, MAX_WHEEL_VELOCITY)

gps = GPS("gps")
gps.enable(TIME_STEP);

camera = Camera("camera")
camera.enable(TIME_STEP);

display = Display("display")

teleoperaton = False #THIS IS ONLY FOR DEBUGGING PURPOSES AND USAGE IN PRODUCTION IS HIGHLY DISCOURAGED. SET THIS TO False WHEN ROVER HAS TO BE AUTONOMOUS.

if teleoperaton == True:
	keyboard = Keyboard();
	keyboard.enable(TIME_STEP);
	cv2.startWindowThread()
	cv2.namedWindow("preview")

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

	gpsLocation = gps.getValues();
	cameraData = camera.getImage();
	image = np.frombuffer(cameraData, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))

	if teleoperaton == True:
		cv2.imshow("preview", image)
		cv2.waitKey(TIME_STEP)