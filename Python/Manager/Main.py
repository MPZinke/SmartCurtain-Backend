#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

###########################################################################
#
#	created by: MPZinke
#	on 01.25.20
#
#	DESCRIPTION:  Master.py is run by a Raspberry Pi/Computer with a DB and local
#		network to serve Slave requests and a PHP web interface. Main file with loop for 
#		Smart Curtain.  Creates threads for each option—Adafruit client, Sunrise open, 
#		Sunset Close & Event Prediction, which are de/activated by the `options` table in DB.
#		This main loop is protected through its own try-catch loop that will restart on failure & 
#		record error in a text log.  Program additionally relies on DBFunctions.py that contains
#		all functions for accessing the DB shared with PHP & Slave.  Definitions.py contains
#		global and defined data.  ErrorWriter.py is used for recording most errors to an error
#		text log—this does not include errors that occur in the Adafruit IO abstracted thread
#		MQTTClient::connect().  For future event creating threads (ie EventPredictor, Sunrise,
#		sunset), if the event is for a time that has already passed, it does not create the event
#	BUGS:		-MQTTClient::connect() can fail without recording errors, but does not crash
#				 thread
#	FUTURE:
#
###########################################################################

from threading import Thread
from time import sleep

from Definitions import *

import AdafruitFeed
import DaytimeEvents
import ErrorWriter
import EventPredictor


def main():
	# program loop
	while True:
		try:
			threads =	[
							Thread(target=AdafruitFeed.start_client_loop),
							Thread(target=DaytimeEvents.sunrise_loop),
							Thread(target=DaytimeEvents.sunset_loop),
							Thread(target=EventPredictor.predictor_loop)
						]
			for thread in threads: thread.start()
			for thread in threads: thread.join()

		except Exception as error:
			try: ErrorWriter.write_error(error)  # doubly protect main program loop
			except: print(error)
		sleep(ERROR_WAIT)  # something messed up; give it time to reset


if __name__ == '__main__':
	main()
