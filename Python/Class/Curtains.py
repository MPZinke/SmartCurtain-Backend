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
from datetime import datetime;
from json import dumps as json_dumps;  # use as to be specific, but do not import too much from json
from typing import Union;

from Class.Events import Events;
from Class.Options import Options;


class Curtains:
	def __init__(self, curtain_query : dict, curtain_events_query : list=[], curtain_options_query : list=[]):
		self._id : int = int(curtain_query["id"]);
		self._current_position : int =	int(curtain_query["current_position"]) if curtain_query["current_position"] \
										else 0;
		self._direction : bool = bool(curtain_query["direction"]);
		self._is_activated : bool = bool(curtain_query["is_activated"]);
		self._last_connection : object = curtain_query["last_connection"];
		self._length : int = int(curtain_query["length"]);
		self._name : str = curtain_query["name"];

		self._CurtainsEvents = [Events(event) for event in curtain_events_query];
		self._CurtainsOptions = [Options(option) for option in curtain_options_query];


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


	def json(self, attributes : list=[], **kw_args) -> str:
		if(attributes): output = {attribute : getattr(self, attribute)() for attribute in attributes};
		else: output =	{
							"id" : self._id,
							"current_position" : self._current_position,
							"direction" : self._direction,
							"is_activated" : self._is_activated,
							"last_connection" : datetime.strftime(self._last_connection, "%Y-%m-%d %H:%M:%S"),
							"length" : self._length,
							"name" : self._name
						}
		for kw in kw_args: output[kw] = kw_args[kw];
		return json_dumps(output);


	# ——————————————————————————————————————————————————————— UI ———————————————————————————————————————————————————————

	def current_position_percent_float(self) -> float:
		return self._current_position * 100 / self._length;


	def current_position_percent_int(self) -> int:
		return int(self._current_position * 100 / self._length);


	def state_string(self) -> str:
		if(self._is_activated): return "Moving";
		return {0 : "Closed", self._length : "Fully Open"}.get(self._current_position, "Open");


	# ——————————————————————————————————————————————————————— DB ———————————————————————————————————————————————————————

	def close(self, cnx, cursor, *, Options_id : Union[int, None]=None, time : object=datetime.now()):
		from Python.DB.DBFunctions import new_Event;
		return new_Event(cnx, cursor, self._id, Options_id, 0, time);


	def open(self, cnx : object, cursor : object, *, desired_position : int=0, 
	  Options_id : Union[int, None]=None, time : object=datetime.now()) -> int:
		from Python.DB.DBFunctions import new_Event;
		if(not desired_position): desired_position = self._length;
		return new_Event(cnx, cursor, self._id, Options_id, desired_position, time);


	def open_percentage(self, cnx : object, cursor : object, *, desired_position : int=0,
	  Options_id : Union[int, None]=None, time : object=datetime.now()) -> int:
		desired_position = int(desired_position * self._length / 100);
		return self.open(cnx, cursor, Options_id=Options_id, desired_position=desired_position, time=time);
