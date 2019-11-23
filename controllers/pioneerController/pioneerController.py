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
emitter = Emitter("emitter")

waypointCounter = 0
waypoints = dict()

image = cv2.imread("../../protos/textures/rover_circuit.jpg")
#with open("../../pathCSV/waypoints.csv", "r") as f:
	#reader = csv.DictReader(f)
	#for row in reader:
		#coordinateX = numpy.interp(row["coordinateX"], [0, image.shape[1] - 1], [params[""], params[""]])
		#coordinateY = numpy.interp(row["coordinateY"], [0, image.shape[0] - 1], [params[""], params[""]])
		#waypoints[row["waypointID"]] = ()

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

	xRover, yRover = gps.getValues()[2], gps.getValues()[0]
	emitter.send((str(xRover) + ", " + str(yRover)).encode('utf-8'))
	
	#print(xRover, yRover)
	cX = 32
	cameragetWidth = 64
	k = (2 * cX - cameragetWidth) / cameragetWidth
	roverHelper.lineFollow(robot, MAX_WHEEL_VELOCITY, k)