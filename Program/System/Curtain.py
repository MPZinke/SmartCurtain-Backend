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

from Other.Class.DBClass import DBClass;
from Other.DB.DBCredentials import *;
from Other.DB.DBFunctions import __CLOSE__, __CONNECT__;
from Other.DB.DBFunctions import SELECT_CurtainsEvents, SELECT_current_CurtainsEvents, SELECT_CurtainsOptions;
import Other.Logger as Logger;
from System.CurtainEvent import CurtainEvent;
from System.CurtainOption import CurtainOption;


class Curtain(DBClass):
	def __init__(self, **curtain_info):
		DBClass.__init__(self, "UPDATE_Curtains", **curtain_info);

		# Get associated relations
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		current_events = SELECT_current_CurtainsEvents(cursor, self._id)
		curtains_options = SELECT_CurtainsOptions(cursor, self._id);
		__CLOSE__(cnx, cursor);

		self._CurtainEvents = {event["id"]: CurtainEvent(**{**event, "Curtain": self}) for event in current_events};
		self._CurtainOptions_dict = {option["Options.id"]: CurtainOption(**option) for option in curtains_options};
		self._CurtainOptions_list = self._CurtainOptions_dict.values();


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————
	# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————

	# Call event destructors, because they are not called simply from leaving scope, which leaves straggling threads.
	def delete_events(self):
		for curtain_event in [value for value in self._CurtainEvents.values()]:
			curtain_event.delete();


	# ——————————————————————————————————— GETTERS/SETTERS::DB COLUMN SIMPLE QUERIES ———————————————————————————————————

	# Overwrite default DBCLass function for getting _id. This prevents it from being able to overwrite the value.
	def id(self) -> int:
		return self._id;


	# ———————————————————————————————————————————————— GETTERS: OBJECTS ————————————————————————————————————————————————

	def CurtainEvents(self) -> dict:
		return self._CurtainEvents;


	# Gets the CurtainOption based on either name or id.
	# Takes a string or an int for the name of the CurtainOption.Option or the id of the CurtainOption.Option.id.
	def CurtainOption(self, CurtainOption: Union[int, str]):
		if(isinstance(CurtainOption, int)): return self._CurtainOptions_dict.get(CurtainOption);
		return self._CurtainOptions_dict.get(self._System.Option_by_name(CurtainOption).id());


	def CurtainOptions(self) -> dict:
		return self._CurtainOptions_dict;


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
		if(CurtainEvents_data): event = CurtainEvent(**{**CurtainEvents_data, "Curtain": self});
		if(not CurtainEvents_data): return None;
		if(event.Curtains_id() != self._id):
			event.delete();
			return None;
		self._CurtainEvents[event.id()] = event;
		return event;


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
