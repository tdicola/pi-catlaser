# Raspberry Pi Cat Laser Toy

Demo of a Raspberry Pi-based cat laser toy that can be controlled through the web.

See the demo on Adafruit's show and tell show:

<iframe width="560" height="315" src="//www.youtube.com/embed/aKMIensR_Lc" frameborder="0" allowfullscreen></iframe>

## Hardware

*	Raspberry Pi connected to a [PCA9685-based servo controller](http://www.adafruit.com/products/815).  See also [this tutorial on using a servo controller with a Raspberry Pi](http://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/hooking-it-up).

*	Two [servos](http://www.adafruit.com/products/169) glued to each other at a right angle so one servo controls rotation left/right and the other controls rotation up/down.

	<a href="http://imgur.com/KukjeZu" title="Mobile Upload"><img src="http://i.imgur.com/KukjeZus.jpg" title="Hosted by imgur.com" alt="Mobile Upload"/></a>

*	Laser diode glued to the servo.  You can [buy one](http://www.adafruit.com/products/1054) or scavenge one from a laser pointer (what I chose to do).

*	Network video camera that outputs an MJPEG video stream.  I use a [this Wansview brand camera](http://www.amazon.com/Wansview-Wireless-Surveillance-Microphone-monitoring/dp/B003LNZ1L6/ref=sr_1_1?ie=UTF8&qid=1378666733&sr=8-1&keywords=wansview), but other brands [like Foscam have MJPEG streams](http://www.ispyconnect.com/man.aspx?n=foscam).

	### Note about cameras and video streams

	You can potentially use other cameras like a webcam or even Raspberry Pi camera but you will need to be careful about the latency and display of the video in a web application.  I tried using H.264 encoded video streamed from both an iPhone and webcam through services such as Ustream, Livestream, and even Amazon CloudFront's flash media server.  Unfortunately in all cases the latency of the video stream was extremely high, on the order of 10-15 seconds.  High latency makes the control of laser over the web impossible.  

	Furthermore if you use a video stream that must be embedded in a web page with an iframe or Flash object (like Ustream, Livestream, Youtube, etc.) you will not easily be able to control targeting from directly clicking on the video.  The problem is that web browsers enforce a strict cross-domain security model where click and mouse move events (among others) over an iframe are not visible to the parent web page.  However I found using an MJPEG stream in an img tag had none of these restrictions and you can detect click events, mouse locations, etc. on the video stream image.

## Software

The following software needs to be installed on the Raspberry-Pi:

*	Python 2.7

*	[Flask](http://flask.pocoo.org/)
	
	Can be installed on Raspbian with pip using these commands:

		sudo apt-get install python-pip
		sudo pip install flask

*	[Adafruit Raspberry Pi Code installed](http://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/adafruit-pi-code) and the Adafruit\_PWM\_Servo\_Driver.py and Adafruit\_I2C.py files copied into the same directory as the pi cat laser code.

*	[I2C setup on the Raspberry Pi](http://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)

## Setup and Usage

### Testing the application outside the Raspberry Pi

For convenience the server can be run from outside the Raspberry Pi on a Windows/Linux/Mac machine (with Python and Flask installed) by executing:

	python server.py test

The test parameter will instruct the server to use a mock servo control class which does not depend on Raspberry Pi-specific libraries and functions.

## Future


## License

This work is licensed under a [Creative Commons Attribution 3.0 Unported License](http://creativecommons.org/licenses/by/3.0/deed.en_US).

<a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.en_US"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by/3.0/88x31.png" /></a>
