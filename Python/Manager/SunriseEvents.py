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

from DB.DBCredentials import *;
from DB.DBFunctions import __CONNECT__, Curtains_ids, CurtainsOptions_for_curtain_and_option;
from ManagerGlobal import *;
from Other.Global import *;
from Other.Global import tomorrow_00_00;
from ZWidget import ZWidget;


class SunriseEvents(ZWidget):
	def __init__(self, System):
		ZWidget.__init__(self, "SunriseEvents");
		self._System = System;


	def sunrise_time(self):
		from astral import Astral

		astr_object = Astral()
		astr_object.solar_depression = "civil"
		return astr_object[CITY].sun(local=True)["sunrise"]


	# Determines sleep time for time to next day.
	# Compliments of https://jacobbridges.github.io/post/how-many-seconds-until-midnight/
	def sleep_time(self) -> int:
		return (tomorrow_00_00() - datetime.now()).seconds;


	def _loop_process(self):
		option_id = self._System.Option_name("Sunrise Open");
		sunrise = self.sunrise_time();

		for curtain_id in self._System.Curtains():
			try:
				curtain = self._System.Curtains()[curtain_id];
				curtain_option = curtain.CurtainsOption(option_id);
				if(not curtain_option.is_on()): continue;

				todays_events = curtain.CurtainsEvents_for_range(earliest=sunrise-5, latest=sunrise+5);
				if(any(event.Options_id() == option_id for event in todays_events)): return;  # no need to duplicate







def main():


if __name__ == "__main__":
	main()
