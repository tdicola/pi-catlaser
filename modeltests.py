import unittest
from model import LaserModel

class LaserModelTests(unittest.TestCase):
	def setUp(self):
		self.servos = TestServos()
		self.model = LaserModel(self.servos, 150, 650, 400)

	def test_setxaxis_getxaxis(self):
		self.model.setXAxis(200)
		self.assertEqual(self.model.getXAxis(), 200)
		self.assertEqual(self.servos.xaxis, 200)

	def test_setyaxis_getyaxis(self):
		self.model.setYAxis(200)
		self.assertEqual(self.model.getYAxis(), 200)
		self.assertEqual(self.servos.yaxis, 200)

	def test_setxaxis_out_of_bounds_raises_valueerror(self):
		self.assertRaises(ValueError, self.model.setXAxis, 10)
		self.assertRaises(ValueError, self.model.setXAxis, 700)

	def test_setyaxis_out_of_bounds_raises_valueerror(self):
		self.assertRaises(ValueError, self.model.setYAxis, 10)
		self.assertRaises(ValueError, self.model.setYAxis, 700)

	def test_axis_defaults_to_400(self):
		self.assertEqual(self.model.getXAxis(), 400)
		self.assertEqual(self.model.getYAxis(), 400)
		self.assertEqual(self.servos.xaxis, 400)
		self.assertEqual(self.servos.yaxis, 400)

	def test_setcalibration_getcalibration(self):
		targetCal = [{'x': 150, 'y': 150}, {'x': 450, 'y': 150}, {'x': 400, 'y': 300}, {'x': 200, 'y': 300}]
		servoCal = [{'x': 10, 'y': 10}, {'x': 50, 'y': 10}, {'x': 50, 'y': 50}, {'x': 10, 'y': 50}]
		self.model.setCalibration(targetCal, servoCal)
		tc, sc = self.model.getCalibration()
		self.assertEqual(tc, targetCal)
		self.assertEqual(sc, servoCal)

	def test_setcalibration_saves_calibration(self):
		targetCal = [{'x': 150, 'y': 150}, {'x': 450, 'y': 150}, {'x': 400, 'y': 300}, {'x': 200, 'y': 300}]
		servoCal = [{'x': 10, 'y': 10}, {'x': 50, 'y': 10}, {'x': 50, 'y': 50}, {'x': 10, 'y': 50}]
		self.model.setCalibration(targetCal, servoCal)
		self.model = LaserModel(self.servos, 150, 650, 400)
		tc, sc = self.model.getCalibration()
		self.assertEqual(tc, targetCal)
		self.assertEqual(sc, servoCal)

	def test_target(self):
		targetCal = [{'x': 190, 'y': 190}, {'x': 555, 'y': 190}, {'x': 480, 'y': 525}, {'x': 240, 'y': 525}]
		servoCal = [{'x': 440, 'y': 298}, {'x': 340, 'y': 298}, {'x': 340, 'y': 220}, {'x': 440, 'y': 220}]
		#targetCal = [{"y": 89, "x": 143}, {"y": 89, "x": 516}, {"y": 437, "x": 447}, {"y": 435, "x": 190}]
		#servoCal = [{"y": 445, "x": 430}, {"y": 352, "x": 428}, {"y": 367, "x": 348}, {"y": 425, "x": 345}]
		self.model.setCalibration(targetCal, servoCal)
		self.model.target(190, 190)
		#self.model.target(144, 90)
		self.assertEqual(self.servos.xaxis, 440)
		self.assertEqual(self.servos.yaxis, 298)


class TestServos(object):
	def __init__(self):
		self.xaxis = 0
		self.yaxis = 0

	def setXAxis(self, value):
		self.xaxis = value

	def setYAxis(self, value):
		self.yaxis = value


if __name__ == '__main__':
	unittest.main()