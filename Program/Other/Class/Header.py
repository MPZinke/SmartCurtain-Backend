#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.23                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime, timedelta;
from flask import session;
from typing import Union;


class Header:
	def __init__(self, system, *, error : str="", success : str="") -> None:
		if("_CURTAIN_current" not in session):
			raise Exception("No curtain set: session curtain id must be set before calling Header instance");

		self._Curtains = system.Curtains();
		self._error : str = error;
		self._success : str = success;
		self._selected_curtain = self._Curtains.get(session["_CURTAIN_current"]);


	def Curtains(self):
		return self._Curtains;


	def error(self) -> str:
		return self._error;


	def success(self) -> str:
		return self._success;


	def selected_curtain(self, Curtains_id : int=None) -> Union[object, None]:
		if(isinstance(Curtains_id, type(None))): return self._selected_curtain;
		if(Curtains_id in self._Curtains): self._selected_curtain = self._Curtains[Curtains_id];


	# —————————————————————————————————————————————————— CONVERSION —————————————————————————————————————————————————— #

	def state_string(self, curtain: object=None):
		if(not curtain): curtain = self._selected_curtain;
		if(curtain.is_activated()): return "Moving";
		return {0: "Closed", 100: "Fully Open"}.get(curtain.current_position_percent_int(), "Open");


	def datetime_to_datetext(self, time: object):
		now = datetime.now();

		today = datetime(year=now.year, month=now.month, day=now.day);
		day = datetime(year=time.year, month=time.month, day=time.day);

		if(today == day): return "Today";
		elif((day - today).days == 1): return "Tomorrow";
		elif((day - today).days < 7): return day.strftime("%A");
		else: return day.strftime("%b %d, %Y");


	def datetime_to_timetext(self, time: object):
		return time.strftime("%I:%M %p");
