class LaserModel(object):
	def __init__(self, servos):
		self.servos = servos
		self.axisMin = 150
		self.axisMax = 650
		# X axis points up/down
		self.setXAxis(400)
		# Y axis points left/right
		self.setYAxis(400)
		# Setup corners of targeting box
		self.targetXBounds = (0.0, 240.0)
		self.targetYBounds  = (0.0, 320.0)
		self.laserXBounds = (150.0, 650.0)
		self.laserTopYBounds = (150.0, 650.0)
		self.laserBottomYBounds = (200.0, 600.0)

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

	def interpolate(self, x, xbounds, x1bounds):
		"""
		Linear interpolation of point x along xmin, xmax to a new point
		between x1min, x1max.
		"""
		return x1bounds[0] + (x1bounds[1] - x1bounds[0])*((x - xbounds[0])/(xbounds[1] - xbounds[0]))

	def target(self, x, y):
		"""
		Map from the targeting coordinate space (rectangle 320x240) to the
		laser coordinate space (parrallelogram wider at top than bottom).
		"""
		laserx = self.interpolate(float(x), self.targetXBounds, self.laserXBounds)
		# Interpolate the Y bounds based on how far up/down the laser is targeting
		laserYBounds = (self.interpolate(float(x), self.targetXBounds, (self.laserTopYBounds[0], self.laserBottomYBounds[0])),
						self.interpolate(float(x), self.targetXBounds, (self.laserTopYBounds[1], self.laserBottomYBounds[1])))
		lasery = self.interpolate(float(y), self.targetYBounds, laserYBounds)
		self.setXAxis(laserx)
		self.setYAxis(lasery)
