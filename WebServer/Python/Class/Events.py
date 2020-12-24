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

from Python.Class.Options import Options;


class Events:
	def __init__(self, event_query):
		self._id : int = event_query["id"];
		self._Option : object = Options	({
											"id" : event_query["Options.id"], "is_current" : event_query["is_current"], 
											"description" : event_query["description"], "name" : event_query["name"]
										});
		self._desired_position : int = event_query["desired_position"];
		self._is_current : bool = bool(event_query["is_current"]);
		self._time : object = event_query["time"];


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self, new_id : int=None) -> Union[int, None]:
		if(isinstance(new_id, type(None))): return self._id;
		self._id = new_id;


	def Options_id__object(self) -> object:
		return self._Option;


	def desired_position(self, new_desired_position : int=None) -> Union[int, None]:
		if(isinstance(new_desired_position, type(None))): return self._desired_position;
		self._desired_position = new_desired_position;


	def is_current(self, new_is_current : bool=None) -> Union[bool, None]:
		if(isinstance(new_is_current, type(None))): return self._is_current;
		self._is_current = new_is_current;


	def time(self, new_time : int=None) -> Union[int, None]:
		if(isinstance(new_time, type(None))): return self._time;
		self._time = new_time;
