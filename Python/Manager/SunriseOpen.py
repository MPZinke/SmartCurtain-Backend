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


from datetime import datetime, timedelta;
import warnings;
from warnings import warn as Warn;

from Class.ZWidget import ZWidget;
from Manager.ManagerGlobal import *;
from Manager.ManagerGlobal import datetime_to_utc;
from Other.Global import *;
from Other.Global import tomorrow_00_00, warning_message;
from Other.Logger import log_error;


class SunriseOpen(ZWidget):
	def __init__(self, System):
		ZWidget.__init__(self, "SunriseOpen", System);

		warnings.formatwarning = warning_message;


	def sunrise_time(self):
		from astral import Astral;

		astr_object = Astral();
		astr_object.solar_depression = "civil";
		return astr_object[CITY].sun(local=True)["sunrise"];


	def sleep_time(self) -> int:
		return (tomorrow_00_00() - datetime.now()).seconds;


	def _loop_process(self):
		sunrise = self.sunrise_time().replace(tzinfo=None);
		if(sunrise < datetime.now()): return Warn("Sunrise has already passed for today. Skipping today");

		option_id = self._System.Option_name("Sunrise Open");
		for curtain_id in self._System.Curtains():
			try:
				curtain = self._System.Curtains()[curtain_id];
				curtain_option = curtain.CurtainsOption(option_id);
				if(not curtain_option.is_on()): continue;

				curtain_buffer_time = 0 if(isinstance(curtain.buffer_time(), type(None))) else curtain.buffer_time();
				buffer_td = timedelta(seconds=curtain_buffer_time / 10 / 2);  # .5: buffer both sides; .10: precision
				if(curtain.CurtainsEvents_for_range(earliest=sunrise-buffer_td, latest=sunrise+buffer_td)):
					Warn("Event already set for sunrise time.");
					continue;  # don't duplicate sunrise

				curtain_option_key_values = curtain_option.CurtainsOptionsKeyValues();
				position = curtain_option_key_values[0].value() if curtain_option_key_values else curtain.length();
				curtain.open(desired_position=position, Options_id=option_id, time=sunrise);

			except Exception as error: log_error(error);
