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


from datetime import datetime;
from typing import Union;

from System.CurtainsEvents import CurtainsEvents;
from System.CurtainsOptions import CurtainsOptions;
from DB.DBCredentials import *;
from DB.DBFunctions import __CONNECT__, current_CurtainsEvents_for_curtain, CurtainsOptions_for_curtain;


class Curtains:
	def __init__(self, curtain_info : dict):
		self._id : int = curtain_info["id"];
		self._current_position : int = curtain_info["current_position"] if curtain_info["current_position"] else 0;
		self._direction : bool = bool(curtain_info["direction"]);
		self._is_activated : bool = bool(curtain_info["is_activated"]);
		self._last_connection : object = curtain_info["last_connection"];
		self._length : int = curtain_info["length"];
		self._name : str = curtain_info["name"];

		_, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		self._CurtainsEvents = {event["id"] : CurtainsEvents(event) \
												for event in current_CurtainsEvents_for_curtain(cursor, self._id)};
		self._CurtainsOptions = {option["id"] : CurtainsOptions(option) \
												for option in CurtainsOptions_for_curtain(cursor, self._id)};
		cursor.close();


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;


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


	def CurtainsEvents(self, CurtainsEvents_id : int):
		return self._CurtainsEvents.get(CurtainsEvents_id);


	def CurtainsEvents(self) -> dict:
		return self._CurtainsEvents;


	def CurtainsOptions(self, CurtainsOptions_id : int):
		return self._CurtainsOptions.get(CurtainsOptions_id);


	def CurtainsOptions(self) -> dict:
		return self._CurtainsOptions;


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self, desired_attrs=[]):
		if(desired_attrs): return {attr : getattr(self, attr)() for attr in desired_attrs};

		attrs = ["_id", "_current_position", "_direction", "_is_activated", "_last_connection", "_length", "_name"];
		class_dict = {attr : getattr(self, attr) for attr in attrs};
		class_dict["_CurtainsEvents"] = {ce : self._CurtainsEvents[cd].dict() for ce in self._CurtainsEvents};
		class_dict["_CurtainsOptions"] = {co : self._CurtainsOptions[co].dict() for co in self._CurtainsOptions};
		return class_dict;


	def print(self, tab=0, next_tab=0):
		attrs = ["_id", "_current_position", "_direction", "_is_activated", "_last_connection", "_length", "_name"];
		for attr in attrs: print('\t'*tab, attr, " : ", getattr(self, attr));
		print('\t'*tab, "_CurtainsEvents : ");
		for event in self._CurtainsEvents: self._CurtainsEvents[event].print(tab+next_tab, next_tab);
		print('\t'*tab, "_CurtainsOptions : ");
		for option in self._CurtainsOptions: self._CurtainsOptions[option].print(tab+next_tab, next_tab);


	# ——————————————————————————————————————————————————————— UI ———————————————————————————————————————————————————————

	def current_position_percent_float(self) -> float:
		return self._current_position * 100 / self._length;


	def current_position_percent_int(self) -> int:
		return int(self._current_position * 100 / self._length);


	def state_string(self) -> str:
		if(self._is_activated): return "Moving";
		return {0 : "Closed", self._length : "Fully Open"}.get(self._current_position, "Open");


	# ——————————————————————————————————————————————————————— DB ———————————————————————————————————————————————————————

	def _new_event(self, *, desired_position : int=0, Options_id : int=None, time : object=datetime.now()) -> int:
		from DB.DBCredentials import DB_USER, DB_PASSWORD, DATABASE;
		from DB.DBFunctions import __CONNECT__, CurtainsEvent, new_Event;
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);

		new_Event_id = new_Event(cnx, cursor, self._id, Options_id, desired_position, time);
		if(new_Event_id): self._CurtainsEvents[new_Event_id] = CurtainsEvents(CurtainsEvent(cursor, new_Event_id));
		return new_Event_id;


	def close(self, *, Options_id : int=None, time : object=datetime.now()):
		return self._new_event(desired_position=0, Options_id=Options_id, time=time);


	def open(self, *, desired_position : int=0, Options_id : int=None, time : object=datetime.now()) -> int:
		return self._new_event(desired_position=desired_position, Options_id=Options_id, time=time);


	def open_percentage(self, *, desired_position : int=0, Options_id : int=None, time : object=datetime.now()) -> int:
		desired_position = int(desired_position * self._length / 100);
		return self._new_event(Options_id=Options_id, desired_position=desired_position, time=time);
