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
from DB.DBFunctions import __CONNECT__, current_CurtainsEvents_for_curtain, CurtainsOptions_for_curtain;
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

		_, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		self._CurtainsEvents = {event["id"] : CurtainsEvents(event) \
												for event in current_CurtainsEvents_for_curtain(cursor, self._id)};
		self._CurtainsOptions = {option["Options.id"] : CurtainsOptions(option) \
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


	# ————————————————————————————————————————————————————— EVENTS —————————————————————————————————————————————————————

	def activate_event(self, desired_position : int=0, event_id : int=0) -> bool:
		from requests import post;

		auto_correct = int(self._CurtainsOptions.get(self._System.Option_name("Auto Correct")).is_on());
		auto_calibrate = int(self._CurtainsOptions.get(self._System.Option_name("Auto Calibrate")).is_on());
		post_json =	{
						"auto calibrate" : auto_calibrate, "auto correct" : auto_correct,
						"current position" : self._current_position, "desired position" : desired_position,
						"event" : event_id, "direction" : int(self._direction), "length" : self._length
					};
		try:
			response = post(url=f"http://{self._ip_address}", json=post_json, timeout=3);
			if(response.status_code != 200): raise Exception(f"Status code for event: {event_id} is invalid");
			if("error" in response.json()): raise Exception(f"Received error message: {response.json()['error']}");
			return True;
		except Exception as error: log_error(error);
		return False;



	# ——————————————————————————————————————————————————————— DB ———————————————————————————————————————————————————————

	def _new_event(self, *, desired_position : int=0, Options_id : int=None, time : object=datetime.now()) -> int:
		# add to DB
		from DB.DBCredentials import DB_USER, DB_PASSWORD, DATABASE;
		from DB.DBFunctions import __CONNECT__, CurtainsEvent, new_Event;
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);

		new_Event_id = new_Event(cnx, cursor, self._id, Options_id, desired_position, time);
		if(new_Event_id): self._CurtainsEvents[new_Event_id] = CurtainsEvents(CurtainsEvent(cursor, new_Event_id));
		# set activation
		if(time <= datetime.now()): return new_Event_id * self.activate_event(desired_position, new_Event_id);
		else:
			pass
			#TODO create an activation thread


	def close(self, *, Options_id : int=None, time : object=datetime.now()):
		return self._new_event(desired_position=0, Options_id=Options_id, time=time);


	def close_immediately(self, Options_id : int=None) -> int:
		return self._new_event(Options_id=Options_id);



	def open(self, *, desired_position : int=0, Options_id : int=None, time : object=datetime.now()) -> int:
		return self._new_event(desired_position=desired_position, Options_id=Options_id, time=time);


	def open_immediately(self, desired_position : int=0, Options_id : int=None) -> int:
		event_id = self._new_event(desired_position=desired_position, Options_id=Options_id);
		if(not event_id): return False;
		
		return 0;


	def open_percentage(self, *, desired_position : int=0, Options_id : int=None, time : object=datetime.now()) -> int:
		desired_position = int(desired_position * self._length / 100);
		return self._new_event(Options_id=Options_id, desired_position=desired_position, time=time);
