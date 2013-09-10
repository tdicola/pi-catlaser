# Raspberry Pi Cat Laser Toy

Demo of a cat laser toy that can be controlled through the web using a Raspberry Pi.  See the demo from Tony on [Adafruit's 9/7/2013 show and tell show](http://www.youtube.com/watch?feature=player_detailpage&v=aKMIensR_Lc#t=745) (~12 minutes into the show)!

The hardware setup:

<a href="http://imgur.com/H2lrnZ7" title="Mobile Upload"><img src="http://i.imgur.com/H2lrnZ7l.jpg" title="Hosted by imgur.com" alt="Mobile Upload"/></a>

The web application.  Clicking in the red target area will aim the laser:

<a href="http://imgur.com/F4eB9sH"><img src="http://i.imgur.com/F4eB9sHl.png" title="Hosted by imgur.com"/></a>

## Hardware

*	Raspberry Pi connected to a [PCA9685-based servo controller](http://www.adafruit.com/products/815).  See [this tutorial on using a servo controller with a Raspberry Pi](http://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/hooking-it-up).

*	Two [servos](http://www.adafruit.com/products/169) glued to each other at a right angle.  One servo controls rotation left/right and the other controls rotation up/down.  See the image below:

	<a href="http://imgur.com/DTGnc2f" title="Mobile Upload"><img src="http://i.imgur.com/DTGnc2fs.jpg" title="Hosted by imgur.com" alt="Mobile Upload"/></a>
	
	Make sure the servos are aimed at roughly the same angle as the camera (to reduce the error between clicking and aiming the laser).

*	Laser diode glued to the servo.  You can [buy one](http://www.adafruit.com/products/1054) or scavenge one from a laser pointer (what I chose to do).

*	Network video camera that outputs an MJPEG video stream.  I use [this Wansview brand camera](http://www.amazon.com/Wansview-Wireless-Surveillance-Microphone-monitoring/dp/B003LNZ1L6/ref=sr_1_1?ie=UTF8&qid=1378666733&sr=8-1&keywords=wansview), but other brands like Foscam [output MJPEG streams](http://www.ispyconnect.com/man.aspx?n=foscam).

	### Note about cameras and video streams

	You can potentially use other cameras like a webcam or even Raspberry Pi camera, but you will need to be careful about the latency and display of the video on the web.  I tried using H.264 encoded video streamed from both an iPhone and webcam through services such as Ustream, Livestream, and even Amazon AWS CloudFront.  Unfortunately in all cases the latency of the video stream was extremely high, on the order of 10-15 seconds.  High latency makes the control of laser over the web impossible.  

	Furthermore if you use a video stream that must be embedded in a web page with an iframe or Flash object (like Ustream, Livestream, Youtube, etc.) you will not be able to target by clicking the video.  The problem is that web browsers enforce a strict cross-domain security model where ovents on an iframe/embedded object are not visible to the parent web page.  Using an MJPEG stream cna work around this restriction because the video is embedded in an image tag.

## Software

The following software needs to be installed on the Raspberry-Pi:

*	Python 2.7

*	[Flask](http://flask.pocoo.org/)
	
	Can be installed on Raspbian using these commands:

		sudo apt-get install python-pip
		sudo pip install flask

*	[NumPy](http://www.numpy.org/)

	Can be installed on Raspbian using this command:

		sudo apt-get install python-numpy

*	[I2C setup on the Raspberry Pi](http://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)

## Setup and Usage

With the software setup, edit server.py to adjust the servo channel, minimum, maximum, etc. values at the top of the file if necessary.  Save the file an execute:

	sudo python server.py

The server should start and you can connect to it from a web browser at http://(IP address of your Raspberry Pi):5000/.  Click the Start Calibration button to walk through the calibration process.  Follow the calibration instructions and click inside the red target area to move the laser.

### Bugs and Limitations

Note the web application only works in Chrome, Safari, and likely Firefox (untested).  Internet Explorer unfortunately does not appear to work because the MJPEG video stream is not visible in an image tag. 

This application is currently designed to run privately within your network or over a VPN.  To support running over the internet work should be done to proxy the video stream and secure the APIs.

### Testing Outside The Raspberry Pi

For convenience the server can be run from outside the Raspberry Pi by executing:

	python server.py test

The test parameter will instruct the server to use a mock servo control class which does not depend on Raspberry Pi-specific libraries and functions.  Make sure the machine this command is running from has Python, Flask, and NumPy installed on it.

## License

Copyright 2013 Tony DiCola

This work is licensed under a [Creative Commons Attribution 3.0 Unported License](http://creativecommons.org/licenses/by/3.0/deed.en_US).

<a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.en_US"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by/3.0/88x31.png" /></a>

The included Adafruit Raspberry Pi servo controller and I2C code is available from [this repository](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code) with the following license:

> Copyright (c) 2012-2013 Limor Fried, Kevin Townsend and Mikey Sklar for Adafruit Industries. All rights reserved.
> 
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. * Neither the name of the nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
