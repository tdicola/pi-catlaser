class LaserModel(object):
	def __init__(self, servos):
		self.servos = servos
		self.axisMin = 150
		self.axisMax = 650
		# X axis points up/down
		self.setXAxis(400)
		# Y axis points left/right
		self.setYAxis(400)

	def validateAxis(self, value):
		try:
			v = int(value)
			if v < self.axisMin or v > self.axisMax:
				raise ValueError()
			return v
		except:
			raise ValueError('Invalid value! Must be a number between %i and %i.' % (self.axisMin, self.axisMax))

	def setXAxis(self, value):
		self.x_axis_value = self.validateAxis(value)
		self.servos.setXAxis(self.x_axis_value)

	def getXAxis(self):
		return self.x_axis_value

	def setYAxis(self, value):
		self.y_axis_value = self.validateAxis(value)
		self.servos.setYAxis(self.y_axis_value)

	def getYAxis(self):
		return self.y_axis_value
