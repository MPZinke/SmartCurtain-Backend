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


from datetime import datetime;
from typing import Union;


class CurtainsEvents:
	def __init__(self, event_info : dict):
		self._id : int = event_info["id"];
		self._Curtains_id : int = event_info["Curtains.id"];
		self._Options_id : int = event_info["Options.id"];
		self._desired_position : int = event_info["desired_position"];
		self._is_current : bool = bool(event_info["is_current"]);
		self._time : object = event_info["time"];


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;


	def Curtains_id(self) -> int:
		return self._Curtains_id;


	def Options_id(self) -> int:
		return self._Options_id;


	def desired_position(self, new_desired_position : Union[int, None]=None) -> Union[int, None]:
		if(isinstance(new_desired_position, type(None))): return self._desired_position;
		self._desired_position = new_desired_position;


	def is_current(self, new_is_current : Union[bool, None]=None) -> Union[bool, None]:
		if(isinstance(new_is_current, type(None))): return self._is_current;
		self._is_current = new_is_current;


	def time(self, new_time : Union[int, None]=None) -> Union[int, None]:
		if(isinstance(new_time, type(None))): return self._time;
		self._time = new_time;


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self):
		attrs = ["_id", "_Curtains_id", "_Options_id", "_desired_position", "_is_current", "_time"];
		return {attr : getattr(self, attr) for attr in attrs};


	def print(self, tab=0, next_tab=0):
		attrs = ["_id", "_Curtains_id", "_Options_id", "_desired_position", "_is_current", "_time"];
		for attr in attrs: print('\t'*tab, attr, " : ", getattr(self, attr));
