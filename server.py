# TODO:

from flask import *
import json
import model, modeltests

DEBUG = True

# Initialize flask app
app = Flask(__name__)
app.config.from_object(__name__)

servos = modeltests.TestServos()
model = model.LaserModel(servos)

# Define views
@app.route('/')
def main():
	return render_template('main.html', model=model)

@app.route('/set/xaxis/<xaxis>', methods=['PUT'])
def setXAxis(xaxis):
	try:
		model.setXAxis(xaxis)
	except ValueError as e:
		return jsonify({'result': e.message}), 500
	return jsonify({'result': 'success'}), 204

@app.route('/set/yaxis/<yaxis>', methods=['PUT'])
def setYAxis(yaxis):
	try:
		model.setYAxis(yaxis)
	except ValueError as e:
		return jsonify({'result': e.message}), 500
	return jsonify({'result': 'success'}), 204

# Start running the flask app
if __name__ == '__main__':
	app.run(host='0.0.0.0')