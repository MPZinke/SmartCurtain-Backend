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
	def __init__(self, system, *, error : str="", success : str=""):
		if("_CURTAIN_current" not in session):
			raise Exception("No curtain set: session curtain id must be set before calling Header instance");

		self._System = system;
		self._Curtains = system.Curtains();
		self._error : str = error;
		self._success : str = success;
		self._selected_curtain = system.Curtain(id=session["_CURTAIN_current"]);


	def Curtains(self) -> list:
		return self._Curtains;


	def error(self) -> str:
		return self._error;


	def success(self) -> str:
		return self._success;


	def selected_curtain(self, Curtains_id: int=None) -> Union[object, None]:
		if(Curtains_id is None):
			return self._selected_curtain;
		if(Curtains_id in self._Curtains):
			self._selected_curtain = self._Curtains[Curtains_id];


	# —————————————————————————————————————————————————— CONVERSION —————————————————————————————————————————————————— #

	def state_string(self, curtain: object=None) -> str:
		if(not curtain):
			curtain = self._selected_curtain;
		if(curtain.is_activated()):
			return "Moving";
		return {0: "Closed", 100: "Fully Open"}.get(curtain.percentage(), "Open");


	def datetime_to_datetext(self, time: object) -> str:
		now = datetime.now();

		today = datetime(year=now.year, month=now.month, day=now.day);
		day = datetime(year=time.year, month=time.month, day=time.day);

		if(today == day): return "Today";
		elif((day - today).days == 1): return "Tomorrow";
		elif((day - today).days < 7): return day.strftime("%A");
		else: return day.strftime("%b %d, %Y");


	def datetime_to_timetext(self, time: object) -> str:
		return time.strftime("%I:%M %p");
