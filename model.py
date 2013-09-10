import json
import numpy as np

class LaserModel(object):
    def __init__(self, servos, servoMin, servoMax, servoCenter):
        self.servos = servos
        self.servoMin = servoMin
        self.servoMax = servoMax
        self.setXAxis(servoCenter)
        self.setYAxis(servoCenter)
        self.targetCalibration = None
        self.servoCalibration = None
        self.transform = None
        self.calibrationFile = 'calibration.json'
        self._loadCalibration()
        self._generateTransform()

    def setXAxis(self, value):
        self.xAxisValue = self._validateAxis(value)
        self.servos.setXAxis(self.xAxisValue)

    def getXAxis(self):
        return self.xAxisValue

    def setYAxis(self, value):
        self.yAxisValue = self._validateAxis(value)
        self.servos.setYAxis(self.yAxisValue)

    def getYAxis(self):
        return self.yAxisValue

    def setCalibration(self, targetCalibration, servoCalibration):
        self.targetCalibration = targetCalibration
        self.servoCalibration = servoCalibration
        self._generateTransform()
        self._saveCalibration()

    def getCalibration(self):
        return self.targetCalibration, self.servoCalibration

    def target(self, x, y):
        """Transform screen coordinate position to servo coordinate position and move servos accordingly."""
        if self.transform == None:
            raise ValueError('Calibration not set!')
        screen = np.array([float(x), float(y), 1.0])
        servo = self.transform.dot(screen)
        servo = servo/servo[2]
        self.setXAxis(round(servo[0]))
        self.setYAxis(round(servo[1]))

    def _validateAxis(self, value):
        """Validate servo value is within range of allowed values."""
        try:
            v = int(value)
            if v < self.servoMin or v > self.servoMax:
                raise ValueError()
            return v
        except:
            raise ValueError('Invalid value! Must be a value between %i and %i.' % (self.servoMin, self.servoMax))

    def _loadCalibration(self):
        """Load calibration data from disk."""
        try:
            with open(self.calibrationFile, 'r') as file:
                cal = json.loads(file.read())
                self.targetCalibration = cal['targetCalibration']
                self.servoCalibration = cal['servoCalibration']
        except IOError:
            pass

    def _saveCalibration(self):
        """Save calibration data to disk."""
        with open(self.calibrationFile, 'w') as file:
            file.write(json.dumps({'targetCalibration': self.targetCalibration, 'servoCalibration': self.servoCalibration }))

    def _generateTransform(self):
        """ 
        Generate the matrix to transform a quadrilaterl in target click coordinates to a quadrilateral in
        servo movement coordinates using a perspective transformation.  
        See http://alumni.media.mit.edu/~cwren/interpolator/ for more details.
        """
        if self.targetCalibration == None or self.servoCalibration == None:
            return
        # Define some variables to make the matrices easier to read
        x1 = float(self.targetCalibration[0]['x'])
        y1 = float(self.targetCalibration[0]['y'])
        x2 = float(self.targetCalibration[1]['x'])
        y2 = float(self.targetCalibration[1]['y'])
        x3 = float(self.targetCalibration[2]['x'])
        y3 = float(self.targetCalibration[2]['y'])
        x4 = float(self.targetCalibration[3]['x'])
        y4 = float(self.targetCalibration[3]['y'])
        X1 = float(self.servoCalibration[0]['x'])
        Y1 = float(self.servoCalibration[0]['y'])
        X2 = float(self.servoCalibration[1]['x'])
        Y2 = float(self.servoCalibration[1]['y'])
        X3 = float(self.servoCalibration[2]['x'])
        Y3 = float(self.servoCalibration[2]['y'])
        X4 = float(self.servoCalibration[3]['x'])
        Y4 = float(self.servoCalibration[3]['y'])
        # Define matrices
        A = np.array([  [x1, y1,  1,  0,  0,  0, -X1*x1, -X1*y1],
                        [ 0,  0,  0, x1, y1,  1, -Y1*x1, -Y1*y1],
                        [x2, y2,  1,  0,  0,  0, -X2*x2, -X2*y2],
                        [ 0,  0,  0, x2, y2,  1, -Y2*x2, -Y2*y2],
                        [x3, y3,  1,  0,  0,  0, -X3*x3, -X3*y3],
                        [ 0,  0,  0, x3, y3,  1, -Y3*x3, -Y3*y3],
                        [x4, y4,  1,  0,  0,  0, -X4*x4, -X4*y4],
                        [ 0,  0,  0, x4, y4,  1, -Y4*x4, -Y4*y4] ])
        B = np.array([X1, Y1, X2, Y2, X3, Y3, X4, Y4])
        # Solve for coefficients x in equation Ax = B
        x = np.linalg.solve(A, B)
        # Set transformation matrix with coefficients
        self.transform = np.array([  [x[0], x[1], x[2]],
                                     [x[3], x[4], x[5]],
                                     [x[6], x[7],  1.0] ])
