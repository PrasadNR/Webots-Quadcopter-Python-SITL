from controller import *
import mavic2proHelper
import cv2
import numpy

TIME_STEP = 64
TAKEOFF_THRESHOLD_VELOCITY = 163

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

k_vertical_thrust = 68.5;
k_vertical_offset = 0.6;
k_vertical_p = 3.0;
k_roll_p = 50.0;
k_pitch_p = 30.0;
target_altitude = 1.0;
roll_disturbance = 0.0;
pitch_disturbance = 0.0;
yaw_disturbance = 0.0;
M_PI = numpy.pi;

while (robot.step(timestep) != -1):

	led_state = int(robot.getTime()) % 2
	front_left_led.set(led_state)
	front_right_led.set(int(not(led_state)))

	roll = imu.getRollPitchYaw()[0] + M_PI/2.0
	pitch = imu.getRollPitchYaw()[1]
	altitude = gps.getValues()[1]
	roll_acceleration = gyro.getValues()[0]
	pitch_acceleration = gyro.getValues()[1]
	camera_roll_motor_position = -0.115 * roll_acceleration
	camera_pitch_motor_position = -0.1 * pitch_acceleration

	if not(numpy.isnan(camera_roll_motor_position)):
		camera_roll_motor.setPosition(camera_roll_motor_position)
	if not(numpy.isnan(camera_pitch_motor_position)):
		camera_pitch_motor.setPosition(camera_pitch_motor_position)

	