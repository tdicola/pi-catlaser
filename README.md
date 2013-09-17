# Raspberry Pi Cat Laser Toy

Demo of a cat laser toy that can be controlled through the web using a Raspberry Pi.  See the demo from Tony on [Adafruit's 9/7/2013 show and tell show](http://www.youtube.com/watch?feature=player_detailpage&v=aKMIensR_Lc#t=745) (~12 minutes into the show)!

The hardware setup:

<a href="http://imgur.com/H2lrnZ7" title="Mobile Upload"><img src="http://i.imgur.com/H2lrnZ7l.jpg" title="Hosted by imgur.com" alt="Mobile Upload"/></a>

The web application.  Clicking in the red target area will aim the laser:

<a href="http://imgur.com/F4eB9sH"><img src="http://i.imgur.com/F4eB9sHl.png" title="Hosted by imgur.com"/></a>

## Guide

This project is now written up as a guide on the [Adafruit Learning System](http://learn.adafruit.com/raspberry-pi-wifi-controlled-cat-laser-toy).  See the guide there for details on how to set up the hardware and software for the project.

### Testing Outside The Raspberry Pi

For convenience the server can be run from outside the Raspberry Pi by executing:

	python server.py test

The test parameter will instruct the server to use a mock servo control class which does not depend on Raspberry Pi-specific libraries and functions.  Make sure the machine this command is running from has Python, Flask, and NumPy installed on it.

## License

Copyright 2013 Tony DiCola

This code is released under an [MIT license](http://opensource.org/licenses/MIT).  See LICENSE.txt for the full details of the license, and the licenses of dependencies that are distributed with this code.
