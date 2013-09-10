class LaserModel(object):
	def __init__(self, servos, servoMin, servoMax, servoCenter):
		self.servos = servos
		self.servoMin = servoMin
		self.servoMax = servoMax
		self.setXAxis(servoCenter)
		self.setYAxis(servoCenter)
		self.targetCalibration = None
		self.servoCalibration = [{'x': servoMin, 'y': servoMin}, {'x': servoMax, 'y': servoMin}, {'x': servoMax, 'y': servoMax}, {'x': servoMin, 'y': servoMax}]

	def validateAxis(self, value):
		try:
			v = int(value)
			if v < self.servoMin or v > self.servoMax:
				raise ValueError()
			return v
		except:
			raise ValueError('Invalid value! Must be a value between %i and %i.' % (self.servoMin, self.servoMax))

	# X axis servo rotation points the laser up/down
	def setXAxis(self, value):
		self.x_axis_value = self.validateAxis(value)
		self.servos.setXAxis(self.x_axis_value)

	def getXAxis(self):
		return self.x_axis_value

	# Y axis servo rotation points the laser left/right
	def setYAxis(self, value):
		self.y_axis_value = self.validateAxis(value)
		self.servos.setYAxis(self.y_axis_value)

	def getYAxis(self):
		return self.y_axis_value
