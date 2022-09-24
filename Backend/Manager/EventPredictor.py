#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.01.18                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION: Daytime events include closing at sundown and opening at sunup. Functionality for creating opening    #
#     events for sunrise. The use of this module requires a CITY definition for geo-location that is in the Astral     #
#     library.  This information is then checked if any events are This information is then checked if any events are  #
#     scheduled soon to it (to prevent double scheduling).  If it nothing is there it will set the event.              #
#   BUGS:        Astral 2.xx does not work. You must use pip3 install astral==1.10.1 (as of 2021.01.18)                #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################

###########################################################################
#
#	created by: MPZinke
#	on ..
#
#	DESCRIPTION: K-Means clustering is used to determine possible events for day based
#		on events for that particular day of week for the last 4 weeks (hard coded).  Events
#		contain the datetime object pulled from the DB, and converts it to a decimal
#		representation of it for smoother calculation  A centroid is created for the ceil(average
#		number of events for that weekdat).  This centroid then finds its surrounding event
#		times over 20 iterations or once all the centroid averages remain constant over 2
#		iterations.  Each centroid then checks if it is valid—3 events within ±30 minutes
#		(hardcoded) of the average.  Commented is code that will find the tightest grouping &
#		check that it is valid, however it is deemed as unnecessary at the moment.  If a
#		centroid is valid, it will average the position of each event and create a new event at
#		that position average.
#	BUGS:
#	FUTURE:
#
###########################################################################


from datetime import datetime, timedelta;
import warnings;
from warnings import warn as Warn;


from Global import *;
from SmartCurtain import SmartCurtain;
from Utility import midnight, warning_message;
from Utility import Logger;
from Utility.ZThread import ZWidget;


class EventTime:
	def __init__(self, eventtime_datetime, position):
		self._datetime = eventtime_datetime;
		self._position = position;


	def decimal(self):
		return self._datetime.hour + self._datetime.minute / 60;


	def position(self):
		return self._position


class EventPredictor(ZWidget):
	def __init__(self, smart_curtain: SmartCurtain):
		ZWidget.__init__(self, "EventPredictor", smart_curtain);

		warnings.formatwarning = warning_message;


	def predicted_events_for_past_events(self, past_events : list) -> list:
		pass


	def _loop_process(self):
		option = self._SmartCurtain.Option(name="Event Predictor");
		for curtain in self._SmartCurtain.Curtains():
			try:
				curtain_option = curtain.CurtainOption(id=option.id());
				if(not curtain_option.is_on()):
					continue;

			except Exception as error:
				Logger.log_error(error);
