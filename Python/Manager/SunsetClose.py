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

from Class.ZWidget import ZWidget;
from Manager.ManagerGlobal import *;
from Manager.ManagerGlobal import datetime_to_utc;
from Other.Global import *;
from Other.Global import tomorrow_00_00, warning_message;
from Other.Logger import log_error;


class SunsetClose(ZWidget):
	def __init__(self, System):
		ZWidget.__init__(self, "SunsetClose", System);

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

		for curtain_id in self._System.Curtains():
			try:
				curtain = self._System.Curtains()[curtain_id];
				curtain_option = curtain.CurtainOption("Sunset Close");
				if(not curtain_option.is_on()): continue;

				curtain_buffer_time = 0 if(isinstance(curtain.buffer_time(), type(None))) else curtain.buffer_time();
				buffer_td = timedelta(seconds=curtain_buffer_time / 10 / 2);  # .5: buffer both sides; .10: precision 
				if(curtain.CurtainEvents_for_range(earliest=sunset-buffer_td, latest=sunset+buffer_td)):
					Warn("Event already set for sunset time.");
					continue;  # don't duplicate sunset

				curtain_option_key_values = curtain_option.CurtainOptionKeyValues();
				position = curtain_option_key_values[0].value() if curtain_option_key_values else 0;
				curtain.open(desired_position=position, Options_id=curtain_option.Options_id(), time=sunset);

			except Exception as error: log_error(error);
