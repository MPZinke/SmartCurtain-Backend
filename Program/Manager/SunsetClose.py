#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.01.18                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION: Daytime events include closing at sundown and opening at sunup. Functionality for creating opening    #
#     events for sunset. The use of this module requires a CITY definition for geo-location that is in the Astral     #
#     library.  This information is then checked if any events are This information is then checked if any events are  #
#     scheduled soon to it (to prevent double scheduling).  If it nothing is there it will set the event.              #
#   BUGS:        Astral 2.xx does not work. You must use pip3 install astral==1.10.1 (as of 2021.01.18)                #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime, timedelta;
import warnings;
from warnings import warn as Warn;

from Global import *;
from Manager.ManagerGlobal import *;
from Utility import time_to_midnight, warning_message;
from Utility import Logger;
from Utility.ZThread import ZWidget;


class SunsetClose(ZWidget):
	def __init__(self, System):
		ZWidget.__init__(self, "SunsetClose", System);

		self._option_id = self._System.Option(name="Sunset Close").id();

		warnings.formatwarning = warning_message;


	def sunset_time(self):
		from astral import Astral;

		astr_object = Astral();
		astr_object.solar_depression = "civil";
		return astr_object[CITY].sun(local=True)["sunset"];


	def sleep_time(self) -> int:
		return time_to_midnight();


	def _loop_process(self):
		sunset = self.sunset_time().replace(tzinfo=None);
		if(sunset < datetime.now()):
			Warn("Sunset has already passed for today. Skipping today");
			return;

		for curtain in self._System.Curtains():
			try:
				curtain_option = curtain.CurtainOption(Options_id=self._option_id);
				if(not curtain_option.is_on()):
					continue;

				curtain_buffer_time = 0 if(isinstance(curtain.buffer_time(), type(None))) else curtain.buffer_time();
				buffer_td = timedelta(seconds=curtain_buffer_time / 10 / 2);  # .5: buffer both sides; .10: precision
				if(curtain.CurtainEvents_for_range(earliest=sunset-buffer_td, latest=sunset+buffer_td)):
					Warn("Event already set for sunset time.");
					continue;  # don't duplicate sunset

				percentage = curtain_option.data() if curtain_option.data() else 0;
				curtain.open(percentage=percentage, Options_id=self._option_id, time=sunset);

			except Exception as error:
				Logger.log_error(error);
