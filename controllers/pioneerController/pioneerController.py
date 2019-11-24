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
M_PI = numpy.pi

[frontLeftMotor, frontRightMotor, backLeftMotor, backRightMotor] = roverHelper.getMotorAll(robot)
MAX_WHEEL_VELOCITY = frontLeftMotor.getMaxVelocity()

timestep = int(robot.getBasicTimeStep())
roverHelper.initialiseMotors(robot, MAX_WHEEL_VELOCITY)

gps = GPS("gps")
gps.enable(TIME_STEP)
emitter = Emitter("emitter")
compass = Compass("compass")
compass.enable(TIME_STEP)

waypointCounter = 0
waypoints = dict()
image = cv2.imread("../../protos/textures/rover_circuit.jpg")

with open("../../pathCSV/waypoints.csv", "r") as f:
	reader = csv.DictReader(f)
	for row in reader:
		coordinateX = numpy.interp(row["coordinateX"], [0, image.shape[1] - 1], [-float(params["floor_width"]) / 2, float(params["floor_width"]) / 2])
		coordinateY = numpy.interp(row["coordinateY"], [0, image.shape[0] - 1], [-float(params["floor_height"]) / 2, float(params["floor_height"]) / 2])
		waypoints[row["waypointID"]] = (coordinateX, coordinateY)

teleoperaton = True #THIS VARIABLE IS ONLY FOR DEBUGGING PURPOSES AND USAGE OF THIS VARIABLE IN PRODUCTION IS HIGHLY DISCOURAGED. SET THIS TO False WHEN ROVER HAS TO BE AUTONOMOUS.

if teleoperaton == True:
	keyboard = Keyboard();
	keyboard.enable(TIME_STEP);

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
	compassValues = compass.getValues()

	xRover, yRover = gps.getValues()[2], gps.getValues()[0]
	emitter.send((str(xRover) + ", " + str(yRover)).encode('utf-8'))
	
	robotHeading = M_PI - numpy.arctan2(compassValues[0], compassValues[2])
	waypointX, waypointY = waypoints[str(waypointCounter)][0], waypoints[str(waypointCounter)][1]
	print(waypointCounter)
	waypointHeading = numpy.arctan2(yRover - waypointY, xRover - waypointX) + M_PI / 2.0
	if waypointHeading < 0:
		waypointHeading = waypointHeading + 2 * M_PI
	
	steering = (robotHeading - waypointHeading) / M_PI
	steering = numpy.clip(steering, -1.0, 1.0)

	if numpy.isnan(steering) == False:
		roverHelper.lineFollow(robot, MAX_WHEEL_VELOCITY, steering)

	roverWaypointDistance = numpy.sqrt((xRover - waypointX) * (xRover - waypointX) + (yRover - waypointY) * (yRover - waypointY))
	
	if roverWaypointDistance < float(params["waypoint_reached_tolerance"]):
		waypointCounter = waypointCounter + 1