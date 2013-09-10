from flask import *
import json, sys

import model

# Flask app configuration
DEBUG = True

# Cat laser toy configuration
SERVO_I2C_ADDRESS 	= 0x40		# I2C address of the PCA9685-based servo controller
SERVO_XAXIS_CHANNEL = 0 		# Channel for the x axis rotation which controls laser up/down
SERVO_YAXIS_CHANNEL = 1			# Channel for the y axis rotation which controls laser left/right
SERVO_PWM_FREQ 		= 50 		# PWM frequency for the servos in HZ (should be 50)
SERVO_MIN 			= 150		# Minimum rotation value for the servo, should be -90 degrees of rotation.
SERVO_MAX 			= 650		# Maximum rotation value for the servo, should be 90 degrees of rotation.
SERVO_CENTER		= 400		# Center value for the servo, should be 0 degrees of rotation.

# Initialize flask app
app = Flask(__name__)
app.config.from_object(__name__)

# Setup the servo and laser model
servos = None
if len(sys.argv) > 1 and sys.argv[1] == "test":
	# Setup test servo for running outside a Raspberry Pi
	import modeltests
	servos = modeltests.TestServos()
else:
	# Setup the real servo when running on a Raspberry Pi
	import servos
	servos = servos.Servos(SERVO_I2C_ADDRESS, SERVO_XAXIS_CHANNEL, SERVO_YAXIS_CHANNEL, SERVO_PWM_FREQ)

model = model.LaserModel(servos, SERVO_MIN, SERVO_MAX, SERVO_CENTER)

# Main view for rendering the web page
@app.route('/')
def main():
	return render_template('main.html', model=model)

# Error handler for API call failures
@app.errorhandler(ValueError)
def valueErrorHandler(error):
	return jsonify({'result': error.message}), 500

def successNoResponse():
	return jsonify({'result': 'success'}), 204

# API calls used by the web app
@app.route('/set/servo/xaxis/<xaxis>', methods=['PUT'])
def setServoXAxis(xaxis):
	model.setXAxis(xaxis)
	return successNoResponse()

@app.route('/set/servo/yaxis/<yaxis>', methods=['PUT'])
def setServoYAaxis(yaxis):
	model.setYAxis(yaxis)
	return successNoResponse()

@app.route('/set/servos/<xaxis>/<yaxis>', methods=['PUT'])
def setServos(xaxis, yaxis):
	model.setXAxis(xaxis)
	model.setYAxis(yaxis)
	return successNoResponse()

@app.route('/get/servos', methods=['GET'])
def getServos():
	return jsonify({'xaxis': model.getXAxis(), 'yaxis': model.getYAxis() }), 200

@app.route('/get/calibration', methods=['GET'])
def getCalibration():
	return jsonify({'target': model.targetCalibration, 'servo': model.servoCalibration}), 200

@app.route('/set/calibration', methods=['POST'])
def setCalibration():
	model.setCalibration(json.loads(request.form['targetCalibration']), json.loads(request.form['servoCalibration']))
	return successNoResponse()

@app.route('/target/<int:x>/<int:y>', methods=['PUT'])
def target(x, y):
	model.target(x, y)
	return successNoResponse()


# Start running the flask app
if __name__ == '__main__':
	app.run(host='0.0.0.0')
