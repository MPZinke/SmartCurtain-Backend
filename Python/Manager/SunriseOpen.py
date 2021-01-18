#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on ..                                                                                                              #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime, timedelta;
from warnings import warn as Warn;

from DB.DBCredentials import *;
from DB.DBFunctions import __CONNECT__, Curtains_ids, CurtainsOptions_for_curtain_and_option;
from Manager.ManagerGlobal import *;
from Other.Global import *;
from Other.Global import tomorrow_00_00;
from Other.Logger import log_error;
from Class.ZWidget import ZWidget;


class SunriseOpen(ZWidget):
	def __init__(self, System):
		ZWidget.__init__(self, "SunriseOpen");
		self._System = System;


	def sunrise_time(self):
		from astral import Astral;

		astr_object = Astral();
		astr_object.solar_depression = "civil";
		return astr_object[CITY].sun(local=True)["sunrise"];


	def sleep_time(self) -> int:
		return (tomorrow_00_00() - datetime.now()).seconds;


	def _loop_process(self):
		option_id = self._System.Option_name("Sunrise Open");
		sunrise = self.sunrise_time();
		if(sunrise < datetime.now()): return Warn("Sunrise has already passed for today. Skipping today");

		for curtain_id in self._System.Curtains():
			try:
				curtain = self._System.Curtains()[curtain_id];
				curtain_option = curtain.CurtainsOption(option_id);
				if(not curtain_option.is_on()): continue;

				TD_5_sec = timedelta(seconds=5);
				todays_events = curtain.CurtainsEvents_for_range(earliest=sunrise-TD_5_sec, latest=sunrise+TD_5_sec);
				if(any(event.Options_id() == option_id for event in todays_events)):
					Warn("Event already set for sunrise time.");
					continue;  # don't duplicate sunrise

				curtain_option_key_values = curtain_option.CurtainsOptionsKeyValues();
				position = curtain_option_key_values[0].value() if curtain_option_key_values else curtain.length();
				curtain.open(desired_position=position, Options_id=option_id, time=sunrise);

			except Exception as error: log_error(error);

