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


from datetime import datetime, timedelta;
from typing import Union;

from Class.DBClass import DBClass;
from DB.DBCredentials import *;
from DB.DBFunctions import __CLOSE__, __CONNECT__;
from DB.DBFunctions import SELECT_CurtainsEvents, SELECT_current_CurtainsEvents, SELECT_CurtainsOptions;
from Other.Logger import log_error;
from System.CurtainEvent import CurtainEvent;
from System.CurtainOption import CurtainOption;


class Curtain(DBClass):
	def __init__(self, **curtain_info):
		DBClass.__init__(self, "UPDATE_Curtains", **curtain_info);

		# Get associated relations
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);

		current_events = SELECT_current_CurtainsEvents(cursor, self._id)
		self._CurtainEvents = {event["id"]: CurtainEvent(**{**event, "Curtain": self}) for event in current_events};

		curtains_options = SELECT_CurtainsOptions(cursor, self._id);
		self._CurtainOptions = {option["Options.id"]: CurtainOption(**option) for option in curtains_options};

		__CLOSE__(cnx, cursor);


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————
	# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————

	# ——————————————————————————————————— GETTERS/SETTERS::DB COLUMN SIMPLE QUERIES ———————————————————————————————————

	# Overwrite default DBCLass function for getting _id. This prevents it from being able to overwrite the value.
	def id(self) -> int:
		return self._id;


	# ———————————————————————————————————————————————— GETTERS: OBJECTS ————————————————————————————————————————————————

	def CurtainEvents(self) -> dict:
		return self._CurtainEvents;


	def CurtainOption(self, Option_identifier: Union[int, str]=None):
		if(type(Option_identifier) == int): return self._CurtainOptions.get(Option_identifier);
		elif(type(Option_identifier) == str):
			options = self._CurtainOptions;
			option = [options[_id] for _id in options if options[_id].name() == Option_identifier];
			return option[0] if len(option)	== 1 else None;


	def CurtainOptionKey(self, CurtainOptionKey: str):
		for option in self._CurtainOptions:
			option_key_value = self._CurtainOptions[option].CurtainOptionKey(CurtainOptionKey);
			if(option_key_value):
				return option_key_value;

		return None;


	def CurtainOptionKeyValue(self, CurtainOptionKeyValue: str):
		for option in self._CurtainOptions:
			option_key_value = self._CurtainOptions[option].CurtainOptionKeyValue(CurtainOptionKeyValue);
			if(option_key_value):
				return option_key_value;

		return None;


	def CurtainOptions(self):
		return self._CurtainOptions;


	def System(self):
		return self._System;


	# ———————————————————————————————————————————————— GETTERS: SPECIAL ————————————————————————————————————————————————

	# Get all curtain events for a time range.
	# Takes the latest datetime time that an event can be, optionally the earliest datetime time an event can be.
	# Cycles through dictionary of events. If an event is within the range, event is added to list.
	# Returns list of curtain events within that time range.
	def CurtainEvents_for_range(self, latest: object=None, earliest: object=None) -> list:
		if(not earliest and not latest): return [self._CurtainEvents[event_id] for event_id in self._CurtainEvents];
		events = [];
		for event_id in self._CurtainEvents:
			event = self._CurtainEvents[event_id];
			if((latest and latest < event.time()) or (earliest and event.time() < earliest)): continue;
			events.append(event);
		return events;


	
	def prior_CurtainEvents_for_current_day_of_week(self, earliest: object=None) -> list:
		earliest = earliest or datetime.today() - timedelta(days=28);

		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		CurtainEvents_data = SELECT_CurtainsEvents(cursor, CurtainsEvents_id);
		__CLOSE__(cnx, cursor);


	# Get CurtainsEvent if exists.
	# Takes the CurtainEvents id to pull from.
	# Checks whether the CurtainEvents exists in memory. If it doesn't, checks if it exists in the DB.
	# Returns the Event if it is found, else None.
	def CurtainEvent(self, CurtainEvent_id: int=None):
		if(CurtainEvent_id in self._CurtainEvents): return self._CurtainEvents.get(CurtainEvent_id);  # easy!

		# not found, check if in DB
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		CurtainEvents_data = SELECT_CurtainsEvents(cursor, CurtainEvent_id);
		__CLOSE__(cnx, cursor);

		# return if found in DB
		if(CurtainEvents_data): event = CurtainEvents(**{**CurtainEvents_data, "Curtain": self});
		if(not CurtainEvents_data or event.Curtains_id() != self._id): return None;
		self._CurtainEvents[event.id()] = event;
		return event;



	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self, desired_attrs=[]):
		ignore_attrs = ["_CurtainsEvents", "_CurtainOptions"];
		if(desired_attrs): return {attr : getattr(self, attr)() for attr in desired_attrs if attr not in ignore_attrs};

		attrs = ["_id", "_current_position", "_direction", "_is_activated", "_last_connection", "_length", "_name"];
		class_dict = {attr : getattr(self, attr) for attr in attrs};
		class_dict["_CurtainsEvents"] = {ce : self._CurtainEvents[cd].dict() for ce in self._CurtainEvents};
		class_dict["_CurtainOptions"] = {co : self._CurtainOptions[co].dict() for co in self._CurtainOptions};
		return class_dict;


	def print(self, tab=0, next_tab=0):
		attrs = ["_id", "_current_position", "_direction", "_is_activated", "_last_connection", "_length", "_name"];
		for attr in attrs: print('\t'*tab, attr, " : ", getattr(self, attr));
		print('\t'*tab, "_CurtainsEvents : ");
		for event in self._CurtainEvents: self._CurtainEvents[event].print(tab+next_tab, next_tab);
		print('\t'*tab, "_CurtainOptions : ");
		for option in self._CurtainOptions: self._CurtainOptions[option].print(tab+next_tab, next_tab);


	# ——————————————————————————————————————————————————————— UI ———————————————————————————————————————————————————————

	def current_position_percent_float(self) -> float:
		return 100 / self._length * self._current_position;


	def current_position_percent_int(self) -> int:
		return int(100 / self._length * self._current_position);


	# ——————————————————————————————————————————————————————— DB ———————————————————————————————————————————————————————

	def _new_event(self, *, desired_position: int=0, Options_id: int=None, time: object=None) -> int:
		if(isinstance(time, type(None))): time = datetime.now();

		kwargs = {"Curtain": self, "Options.id": Options_id, "desired_position": desired_position, "time": time};
		new_CurtainEvent = CurtainEvent.New(**kwargs);
		self._CurtainEvents[new_CurtainEvent.id()] = new_CurtainEvent;

		return new_CurtainEvent.id();


	def close(self, *, Options_id: int=None, time: object=None):
		if(isinstance(time, type(None))): time = datetime.now();

		return self._new_event(desired_position=0, Options_id=Options_id, time=time);


	def close_immediately(self, Options_id : int=None) -> int:
		return self._new_event(Options_id=Options_id);


	def open(self, *, desired_position: int=0, Options_id: int=None, time: object=None) -> int:
		if(isinstance(time, type(None))): time = datetime.now();

		return self._new_event(desired_position=desired_position, Options_id=Options_id, time=time);


	def open_immediately(self, desired_position: int=0, Options_id: int=None) -> int:
		CurtainEvent_id = self._new_event(desired_position=desired_position, Options_id=Options_id);
		return CurtainEvent_id if CurtainEvent_id else False;


	def open_percentage(self, *, desired_position: int=0, Options_id: int=None, time: object=None) -> int:
		if(isinstance(time, type(None))): time = datetime.now();

		desired_position = int(desired_position * self._length / 100);
		return self._new_event(Options_id=Options_id, desired_position=desired_position, time=time);
