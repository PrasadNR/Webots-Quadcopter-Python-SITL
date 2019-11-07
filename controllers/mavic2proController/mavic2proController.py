from controller import *
import mavic2proHelper
import cv2
import numpy
from simple_pid import PID
import csv

target_altitude = 1.0;
targetX = 1.0
targetY = 1.0

params = dict()
with open("params.csv", "r") as f:
	lines = csv.reader(f)
	for line in lines:
		params[line[0]] = line[1]

TIME_STEP = int(params["TIME_STEP"])
TAKEOFF_THRESHOLD_VELOCITY = int(params["TAKEOFF_THRESHOLD_VELOCITY"])
M_PI = numpy.pi;

robot = Robot()

[frontLeftMotor, frontRightMotor, backLeftMotor, backRightMotor] = mavic2proHelper.getMotorAll(robot)
MAX_PROPELLER_VELOCITY = int(frontLeftMotor.getMaxVelocity())

timestep = int(robot.getBasicTimeStep())
mavic2proMotors = mavic2proHelper.getMotorAll(robot)
mavic2proHelper.initialiseMotors(robot, 0)
mavic2proHelper.motorsSpeed(robot, TAKEOFF_THRESHOLD_VELOCITY, TAKEOFF_THRESHOLD_VELOCITY, TAKEOFF_THRESHOLD_VELOCITY, TAKEOFF_THRESHOLD_VELOCITY)

camera = Camera("camera")
camera.enable(TIME_STEP)
front_left_led = LED("front left led")
front_right_led = LED("front right led")
imu = InertialUnit("inertial unit")
imu.enable(TIME_STEP)
gps = GPS("gps")
gps.enable(TIME_STEP)
compass = Compass("compass")
compass.enable(TIME_STEP)
gyro = Gyro("gyro")
gyro.enable(TIME_STEP)
camera_roll_motor = robot.getMotor("camera roll")
camera_pitch_motor = robot.getMotor("camera pitch")

k_vertical_thrust, k_roll_p, k_pitch_p = float(params["k_vertical_thrust"]), float(params["k_roll_p"]), float(params["k_pitch_p"])

pitchPID = PID(float(params["pitch_Kp"]), float(params["pitch_Ki"]), float(params["pitch_Kd"]), setpoint=targetY)
rollPID = PID(float(params["roll_Kp"]), float(params["roll_Ki"]), float(params["roll_Kd"]), setpoint=targetX)
throttlePID = PID(float(params["throttle_Kp"]), float(params["throttle_Ki"]), float(params["throttle_Kd"]), setpoint=target_altitude)
yawPID = PID(float(params["yaw_Kp"]), float(params["yaw_Ki"]), float(params["yaw_Kd"]), setpoint=float(params["yaw_setpoint"]))

while (robot.step(timestep) != -1):

	led_state = int(robot.getTime()) % 2
	front_left_led.set(led_state)
	front_right_led.set(int(not(led_state)))

	roll = imu.getRollPitchYaw()[0] + M_PI / 2.0
	pitch = imu.getRollPitchYaw()[1]
	yaw = compass.getValues()[1]
	altitude = gps.getValues()[1]
	roll_acceleration = gyro.getValues()[0]
	pitch_acceleration = gyro.getValues()[1]

	vertical_input = throttlePID(altitude)
	yaw_input = yawPID(yaw)
	
	x = gps.getValues()[2]
	y = gps.getValues()[0]
	
	roll_input = k_roll_p * roll + roll_acceleration + rollPID(float(params["xPositionFactor"]) * targetX - x)
	pitch_input = k_pitch_p * pitch - pitch_acceleration + pitchPID(y)

	print(x, y)

	front_left_motor_input = k_vertical_thrust + vertical_input - roll_input - pitch_input + yaw_input
	front_right_motor_input = k_vertical_thrust + vertical_input + roll_input - pitch_input - yaw_input
	rear_left_motor_input = k_vertical_thrust + vertical_input - roll_input + pitch_input - yaw_input
	rear_right_motor_input = k_vertical_thrust + vertical_input + roll_input + pitch_input + yaw_input

	if not(numpy.isnan(front_left_motor_input)):
		mavic2proHelper.motorsSpeed(robot, front_left_motor_input, -front_right_motor_input, -rear_left_motor_input, rear_right_motor_input)