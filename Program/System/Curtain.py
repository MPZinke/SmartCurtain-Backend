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
from typing import List, Union;


from Global import NONETYPE;
from System.CurtainEvent import CurtainEvent;
from System.CurtainOption import CurtainOption;
from Utility.DBClass import DBClass;
from Utility.DB import SELECT_CurtainsEvents_for_Curtains_id, SELECT_CurtainsEvents, SELECT_current_CurtainsEvents, \
  SELECT_CurtainsOptions;
from Utility import Logger;
from Utility.DBClass import AttributeType;


class Curtain(DBClass):
	def __init__(self, **curtain_info):
		DBClass.__init__(self, "UPDATE_Curtains", **curtain_info);

		# Get associated relations
		current_events = SELECT_current_CurtainsEvents(self._id);
		curtains_options = SELECT_CurtainsOptions(self._id);

		self.attribute_types: AttributeType =	[
													AttributeType("_id", int),
													AttributeType("_buffer_time", [int, bool, NONETYPE]),
													AttributeType("_percentage", [int, NONETYPE]),
													AttributeType("_direction", [int, bool, NONETYPE]),
													AttributeType("_ip_address", [str, NONETYPE]),
													AttributeType("_is_activated", [int, bool, NONETYPE]),
													AttributeType("_is_current", [int, bool, NONETYPE]),
													AttributeType("_is_safe", [int, bool, NONETYPE]),
													AttributeType("_is_smart", [int, bool, NONETYPE]),
													AttributeType("_port", [int, bool, NONETYPE]),
													AttributeType("_length", [int, bool, NONETYPE]),
													AttributeType("_name", [str])
												];
		self.validate();

		self._CurtainEvents = [CurtainEvent(**{**event, "Curtain": self}) for event in current_events];
		self._CurtainOptions = [CurtainOption(**option) for option in curtains_options];


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————
	# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————

	# Call event destructors, because they are not called simply from leaving scope, which leaves straggling threads.
	def delete_events(self):
		for curtain_event in self._CurtainEvents:
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
	def CurtainOption(self, **kwargs: dict) -> CurtainOption:
		from System.System import System;
		return System._exclusive_match(self._CurtainOptions, **kwargs);


	def CurtainOptions(self) -> List[CurtainOption]:
		return self._CurtainOptions;


	def System(self):
		return self._System;


	# ———————————————————————————————————————————————— GETTERS: SPECIAL ————————————————————————————————————————————————

	# Get all curtain events for a time range.
	# Takes the latest datetime time that an event can be, optionally the earliest datetime time an event can be.
	# Cycles through dictionary of events. If an event is within the range, event is added to list.
	# Returns list of curtain events within that time range.
	def CurtainEvents_for_range(self, latest: object=None, earliest: object=None) -> list:
		if(not earliest and not latest):
			return [self._CurtainEvents[event_id] for event_id in self._CurtainEvents];

		events = [];
		for event in self._CurtainEvents:
			if((latest and latest < event.time()) or (earliest and event.time() < earliest)):
				continue;
			events.append(event);
		return events;


	def prior_CurtainEvents_for_current_day_of_week(self, earliest: object=None) -> list:
		earliest = earliest or datetime.today() - timedelta(days=28);

		#TODO: Get events for day of week.
		CurtainEvents_data = SELECT_CurtainsEvents();


	# Get CurtainsEvent if exists.
	# Takes the CurtainEvents id to pull from.
	# Checks whether the CurtainEvents exists in memory. If it doesn't, checks if it exists in the DB.
	# Returns the Event if it is found, else None.
	def CurtainEvent(self, **kwargs: dict) -> Union[CurtainEvent, None]:
		from System.System import System;
		if((curtain_event := System._exclusive_match(self._CurtainEvents, **kwargs)) is not None):
			return curtain_event;

		# Not found, check if in DB
		if((curtain_events := SELECT_CurtainsEvents_for_Curtains_id(self._id))):
			for event in curtain_events:
				# If found in DB, create an object and add to the list
				if(all(event.get(key) == value for key, value in kwargs)):
					curtain_event = CurtainEvent(**{**event, "Curtain": self});
					self._CurtainEvents.append(curtain_event);
					return curtain_event;

		return None


	# ——————————————————————————————————————————————————————— DB ———————————————————————————————————————————————————————

	def _new_event(self, *, percentage: int=0, Options_id: int=None, time: object=None) -> int:
		if(isinstance(time, type(None))):
			time = datetime.now();

		kwargs = {"Curtain": self, "Options.id": Options_id, "percentage": percentage, "time": time};
		new_CurtainEvent = CurtainEvent.New(**kwargs);
		self._CurtainEvents[new_CurtainEvent.id()] = new_CurtainEvent;

		return new_CurtainEvent.id();


	def close(self, *, Options_id: int=None, time: object=None):
		if(isinstance(time, type(None))):
			time = datetime.now();

		return self._new_event(percentage=0, Options_id=Options_id, time=time);


	def close_immediately(self, Options_id : int=None) -> int:
		return self._new_event(Options_id=Options_id);


	def open(self, *, percentage: int=0, Options_id: int=None, time: object=None) -> int:
		if(isinstance(time, type(None))):
			time = datetime.now();

		return self._new_event(percentage=percentage, Options_id=Options_id, time=time);


	def open_immediately(self, percentage: int=100, Options_id: int=None) -> int:
		CurtainEvent_id = self._new_event(percentage=percentage, Options_id=Options_id);
		return CurtainEvent_id if CurtainEvent_id else False;


	def open_percentage(self, *, percentage: int=100, Options_id: int=None, time: object=None) -> int:
		if(isinstance(time, type(None))):
			time = datetime.now();

		return self._new_event(Options_id=Options_id, percentage=percentage, time=time);
