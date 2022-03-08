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
from Manager.ManagerGlobal import datetime_to_utc;
from Utility import tomorrow_00_00, warning_message;
import Utility.Logger as Logger;
from Utility.ZThread import ZWidget;


class SunsetClose(ZWidget):
	def __init__(self, System):
		ZWidget.__init__(self, "SunsetClose", System);

		self._option_id = self._System.Option_by_name("Sunrise Open").id();

		warnings.formatwarning = warning_message;


	def sunset_time(self):
		from astral import Astral;

		astr_object = Astral();
		astr_object.solar_depression = "civil";
		return astr_object[CITY].sun(local=True)["sunset"];


	def sleep_time(self) -> int:
		return (tomorrow_00_00() - datetime.now()).seconds;


	def _loop_process(self):
		sunset = self.sunset_time().replace(tzinfo=None);
		if(sunset < datetime.now()): return Warn("Sunset has already passed for today. Skipping today");

		for curtain in self._System.Curtains_list():
			try:
				curtain_option = curtain.CurtainOption(self._option_id);
				if(not curtain_option.is_on()): continue;

				curtain_buffer_time = 0 if(isinstance(curtain.buffer_time(), type(None))) else curtain.buffer_time();
				buffer_td = timedelta(seconds=curtain_buffer_time / 10 / 2);  # .5: buffer both sides; .10: precision 
				if(curtain.CurtainEvents_for_range(earliest=sunset-buffer_td, latest=sunset+buffer_td)):
					Warn("Event already set for sunset time.");
					continue;  # don't duplicate sunset

				percentage = curtain_option.data() if curtain_option.data() else 0;
				curtain.open(desired_percentage=percentage, Options_id=self._option_id, time=sunset);

			except Exception as error:
				Logger.log_error(error);
