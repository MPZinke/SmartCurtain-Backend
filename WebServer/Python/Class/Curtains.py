#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.19                                                                                                              #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from copy import deepcopy;
from typing import Union;

from Python.Class.Events import Events;
from Python.Class.Options import Options;


class Curtains:
	def __init__(self, curtain_query, curtain_events_query, curtain_options_query):
		self._id : int = curtain_query["id"];
		self._current_position : int = curtain_query["current_position"];
		self._direction : bool = curtain_query["direction"];
		self._is_activated : bool = curtain_query["is_activated"];
		self._last_connection : object = curtain_query["last_connection"];
		self._length : int = curtain_query["length"];
		self._name : str = curtain_query["name"];

		self._CurtainsEvents = [Events(event) for event in curtain_events_query];
		self._CurtainsOptions = [Options(option) for option in curtain_options_query];


	def current_state_percentage(self) -> float:
		return self._current_position * 100 / self._length;


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self, new_id : int=None) -> Union[int, None]:
		if(isinstance(new_id, type(None))): return self._id;
		self._id = new_id;


	def current_position(self, new_current_position : int=None) -> Union[int, None]:
		if(isinstance(new_current_position, type(None))): return self._current_position;
		self._current_position = new_current_position;


	def direction(self, new_direction : bool=None) -> Union[bool, None]:
		if(isinstance(new_direction, type(None))): return self._direction;
		self._direction = new_direction;


	def is_activated(self, new_is_activated : bool=None) -> Union[bool, None]:
		if(isinstance(new_is_activated, type(None))): return self._is_activated;
		self._is_activated = new_is_activated;


	def last_connection(self, new_last_connection : object=None) -> Union[object, None]:
		if(isinstance(new_last_connection, type(None))): return self._last_connection;
		self._last_connection = new_last_connection;


	def length(self, new_length : int=None) -> Union[int, None]:
		if(isinstance(new_length, type(None))): return self._length;
		self._length = new_length;


	def name(self, new_name : str=None) -> Union[str, None]:
		if(isinstance(new_name, type(None))): return self._name;
		self._name = new_name;


	def CurtainsEvents(self) -> list:
		return deepcopy(self._CurtainsEvents);


	def CurtainsOptions(self) -> list:
		return deepcopy(self._CurtainsOptions);

