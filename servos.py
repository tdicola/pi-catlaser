from Adafruit_PWM_Servo_Driver import PWM

class Servos(object):
	def __init__(self):
		self.pwm = PWM(0x40, debug=True)
		self.pwm.setPWMFreq(50)

	def setXAxis(self, value):
		self.pwm.setPWM(0, 0, value)

	def setYAxis(self, value):
		self.pwm.setPWM(1, 0, value)