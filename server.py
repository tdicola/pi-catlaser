# TODO:
# - error checking tests for target?
# - clean up set and target functions below so they don't duplicate code
# - bug: need correct bounds error message when target fails because input is outside range

from flask import *
import json, sys
import model

DEBUG = True

# Initialize flask app
app = Flask(__name__)
app.config.from_object(__name__)

servos = None
if len(sys.argv) > 1 and sys.argv[1] == "test":
	import modeltests
	servos = modeltests.TestServos()
else:
	import servos
	servos = servos.Servos()

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

@app.route('/setboth/<xaxis>/<yaxis>', methods=['PUT'])
def setBoth(xaxis, yaxis):
	try:
		model.setXAxis(xaxis)
		model.setYAxis(yaxis)
	except ValueError as e:
		return jsonify({'result': e.message}), 500
	return jsonify({'result': 'sucssess'}), 204

@app.route('/get', methods=['GET'])
def get():
	return jsonify({'xaxis': model.getXAxis(), 'yaxis': model.getYAxis() }), 200

@app.route('/target/<xaxis>/<yaxis>', methods=['PUT'])
def target(xaxis, yaxis):
	try:
		model.target(xaxis, yaxis)
	except ValueError as e:
		return jsonify({'result': e.message}), 500
	return jsonify({'result': 'success'}), 204

# Start running the flask app
if __name__ == '__main__':
	app.run(host='0.0.0.0')