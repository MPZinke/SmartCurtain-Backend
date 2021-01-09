#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.19                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime;
from typing import Union;

from DB.DBCredentials import *;
from DB.DBFunctions import __CLOSE__, __CONNECT__;
from Other.Logger import log_error;
from System.CurtainsEvents import CurtainsEvents;
from System.CurtainsOptions import CurtainsOptions;


class Curtains:
	def __init__(self, curtain_info : dict, System):
		self._System = System;

		self._id : int = curtain_info["id"];
		self._current_position : int = curtain_info["current_position"] if curtain_info["current_position"] else 0;
		self._direction : bool = bool(curtain_info["direction"]);
		self._is_activated : bool = bool(curtain_info["is_activated"]);
		self._ip_address : str = curtain_info["ip_address"];
		self._port : int = curtain_info["port"];
		self._last_connection : object = curtain_info["last_connection"];
		self._length : int = curtain_info["length"];
		self._name : str = curtain_info["name"];
		self._CurtainsEvents = None;
		self._CurtainsOptions = None;

		# add CurtainsEvents & CurtainsOptions
		from DB.DBFunctions import current_CurtainsEvents, CurtainsOptions as DBCurtainsOptions;
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		curtains_current_events = current_CurtainsEvents(cursor, self._id)
		self._CurtainsEvents = {event["id"] : CurtainsEvents(event, self) for event in curtains_current_events};
		curtains_options = DBCurtainsOptions(cursor, self._id);
		self._CurtainsOptions = {option["Options.id"] : CurtainsOptions(option) for option in curtains_options};
		__CLOSE__(cnx, cursor);


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;


	def current_position(self, new_current_position : int=None) -> Union[int, bool, None]:
		if(isinstance(new_current_position, type(None))): return self._current_position;
		if(new_current_position == self._current_position): return True;

		from DB.DBFunctions import set_Curtain_current_position;
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		success_flag = set_Curtain_current_position(cnx, cursor, self._id, new_current_position);
		if(success_flag): self._current_position = new_current_position;
		return success_flag + bool(__CLOSE__(cnx, cursor));


	def direction(self, new_direction : bool=None) -> Union[bool, None]:
		if(isinstance(new_direction, type(None))): return self._direction;
		self._direction = new_direction;


	def ip_address(self, new_ip_address : str=None):
		if(isinstance(new_ip_address, type(None))): return self._ip_address;
		print("Hello from here");
		if(new_ip_address == self._ip_address): return True;

		from DB.DBFunctions import set_Curtain_ip_address;
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		success_flag = set_Curtain_ip_address(cnx, cursor, self._id, new_ip_address);
		if(success_flag): self._ip_address = new_ip_address;
		return success_flag + bool(__CLOSE__(cnx, cursor));


	def is_activated(self, new_is_activated : bool=None) -> Union[bool, None]:
		from DB.DBFunctions import set_Curtain_activation;
		if(isinstance(new_is_activated, type(None))): return self._is_activated;

		if(new_is_activated == self._is_activated): return True;

		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		success_flag = set_Curtain_activation(cnx, cursor, self._id, new_is_activated);
		if(success_flag): self._is_activated = new_is_activated;
		return success_flag + bool(__CLOSE__(cnx, cursor));


	def last_connection(self, new_last_connection : object=None) -> Union[object, None]:
		if(isinstance(new_last_connection, type(None))): return self._last_connection;
		self._last_connection = new_last_connection;


	def length(self, new_length : int=None) -> Union[int, None]:
		from DB.DBFunctions import set_Curtain_length;
		if(isinstance(new_length, type(None))): return self._length;

		if(new_length == self._length): return True;

		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		success_flag = set_Curtain_length(cnx, cursor, self._id, new_length);
		if(success_flag): self._length = new_length;
		return success_flag + bool(__CLOSE__(cnx, cursor));


	def name(self, new_name : str=None) -> Union[str, None]:
		if(isinstance(new_name, type(None))): return self._name;
		self._name = new_name;


	def CurtainsEvent(self, CurtainsEvents_id : int=None):
		if(self._CurtainsEvents.get(CurtainsEvents_id)): return self._CurtainsEvents.get(CurtainsEvents_id);  # easy!

		from DB.DBFunctions import CurtainsEvent;
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		CurtainsEvents_data = CurtainsEvent(cursor, CurtainsEvents_id);
		__CLOSE__(cnx, cursor);

		event = CurtainsEvents(CurtainsEvents_data, self) if CurtainsEvents_data else None;
		if(not CurtainsEvents_data or event.Curtains_id() != self._id): return None;
		self._CurtainsEvents[event.id()] = event;
		return event;


	def CurtainsEvents(self) -> dict:
		return self._CurtainsEvents;


	def CurtainsOption(self, CurtainsOptions_id : int=None):
		return self._CurtainsOptions.get(CurtainsOptions_id);


	def CurtainsOptions(self):
		return self._CurtainsOptions;


	def System(self):
		return self._System;


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self, desired_attrs=[]):
		ignore_attrs = ["_CurtainsEvents", "_CurtainsOptions"];
		if(desired_attrs): return {attr : getattr(self, attr)() for attr in desired_attrs if attr not in ignore_attrs};

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
		# add to DB
		from DB.DBFunctions import CurtainsEvent, new_Event;
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);

		new_Event_id = new_Event(cnx, cursor, self._id, Options_id, desired_position, time);
		if(not new_Event_id): return __CLOSE__(cnx, cursor);
		self._CurtainsEvents[new_Event_id] = CurtainsEvents(CurtainsEvent(cursor, new_Event_id), self);
		__CLOSE__(cnx, cursor);

		return new_Event_id;


	def close(self, *, Options_id : int=None, time : object=datetime.now()):
		return self._new_event(desired_position=0, Options_id=Options_id, time=time);


	def close_immediately(self, Options_id : int=None) -> int:
		return self._new_event(Options_id=Options_id);


	def open(self, *, desired_position : int=0, Options_id : int=None, time : object=datetime.now()) -> int:
		return self._new_event(desired_position=desired_position, Options_id=Options_id, time=time);


	def open_immediately(self, desired_position : int=0, Options_id : int=None) -> int:
		CurtainsEvents_id = self._new_event(desired_position=desired_position, Options_id=Options_id);
		if(not CurtainsEvents_id): return False;
		
		return 0;


	def open_percentage(self, *, desired_position : int=0, Options_id : int=None, time : object=datetime.now()) -> int:
		desired_position = int(desired_position * self._length / 100);
		return self._new_event(Options_id=Options_id, desired_position=desired_position, time=time);
