def motorsSpeed(robot, v1, v2, v3, v4):
	frontLeftMotor = robot.getMotor('front left wheel')
	frontRightMotor = robot.getMotor('front right wheel')
	backLeftMotor = robot.getMotor('back left wheel')
	backRightMotor = robot.getMotor('back right wheel')

	frontLeftMotor.setVelocity(v1)
	frontRightMotor.setVelocity(v2)
	backLeftMotor.setVelocity(v3)
	backRightMotor.setVelocity(v4)
	return

class movement:

	def forward(robot, MAX_WHEEL_VELOCITY):
		motorsSpeed(robot, MAX_WHEEL_VELOCITY, MAX_WHEEL_VELOCITY, MAX_WHEEL_VELOCITY, MAX_WHEEL_VELOCITY)
		return

	def backward(robot, MAX_WHEEL_VELOCITY):
		motorsSpeed(robot, -MAX_WHEEL_VELOCITY, -MAX_WHEEL_VELOCITY, -MAX_WHEEL_VELOCITY, -MAX_WHEEL_VELOCITY)
		return

	def left(robot, MAX_WHEEL_VELOCITY):
		motorsSpeed(robot, -MAX_WHEEL_VELOCITY, MAX_WHEEL_VELOCITY, -MAX_WHEEL_VELOCITY, MAX_WHEEL_VELOCITY)
		return

	def right(robot, MAX_WHEEL_VELOCITY):
		motorsSpeed(robot, MAX_WHEEL_VELOCITY, -MAX_WHEEL_VELOCITY, MAX_WHEEL_VELOCITY, -MAX_WHEEL_VELOCITY)
		return

	def brake(robot, MAX_WHEEL_VELOCITY):
		motorsSpeed(robot, 0, 0, 0, 0)
		return

def initialiseMotors(robot, MAX_WHEEL_VELOCITY):
	frontLeftMotor = robot.getMotor('front left wheel')
	frontRightMotor = robot.getMotor('front right wheel')
	backLeftMotor = robot.getMotor('back left wheel')
	backRightMotor = robot.getMotor('back right wheel')

	frontLeftMotor.setPosition(float('inf'))
	frontRightMotor.setPosition(float('inf'))
	backLeftMotor.setPosition(float('inf'))
	backRightMotor.setPosition(float('inf'))

	movement.brake(robot, MAX_WHEEL_VELOCITY)
	return