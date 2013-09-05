import threading, time
import RPi.GPIO as GPIO

class PhotoCell(object):
	def __init__(self, RCpin):
		# Setup GPIO
		GPIO.setmode(GPIO.BCM)
		self.gpioLock = threading.Lock()
		self.RCpin = RCpin

	def getReading(self):
		# Use a lock to serialize access to GPIO so there aren't race conditions with
		# multiple request threads.
		with self.gpioLock:
			reading = 0
			# Set IO line to low
			GPIO.setup(self.RCpin, GPIO.OUT)
			GPIO.output(self.RCpin, GPIO.LOW)
			time.sleep(0.1)
			# Measure how long it takes for capacitor to recharge.
			# This will be proportional to resistance of the sensor.
			GPIO.setup(self.RCpin, GPIO.IN)
			while (GPIO.input(self.RCpin) == GPIO.LOW):
				reading += 1
			return reading