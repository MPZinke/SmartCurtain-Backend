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
from json import dumps;
import os;
import requests;
from typing import List, TypeVar, Union;


from Global import NONETYPE;
from SmartCurtain.CurtainOption import CurtainOption;
from SmartCurtain.DB import DBFunctions;


Curtain = TypeVar("Curtain")
Hub = TypeVar("Hub")


class Curtain:
	def __init__(self, hub: Hub, *, id: int, buffer_time: int, is_deleted: bool, curtain_events: list[CurtainEvent],
	  curtain_options: list[CurtainOption], name: str
	):
		# STRUCTURE #
		self._hub = hub
		# DATABASE #
		self._id: int = id
		self._buffer_time: int = buffer_time
		self._is_deleted: bool = is_deleted
		self._curtain_events: list[CurtainEvent] = curtain_events
		self._curtain_options: list[CurtainOption] = curtain_options
		self._name: str = name
		# TEMP STATE #
		self._is_moving: bool = False
		self._percentage: int = 0


	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"buffer_time": self._buffer_time,
			"is_deleted": self._is_deleted,
			"curtain_events": list(map(dict, self._curtain_events)),
			"curtain_options": list(map(dict, self._curtain_options)),
			"name": self._name,
			"is_moving": self._is_moving,
			"percentage": self._percentage
		}.items();


	def __repr__(self) -> str:
		return str(self);


	def __str__(self) -> str:
		return dumps(dict(self), default=str);


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————
	# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————

	# Call event destructors, because they are not called simply from leaving scope, which leaves straggling threads.
	def delete_events(self):
		for curtain_event in self._CurtainEvents:
			curtain_event.delete();


	# ——————————————————————————————————————— GETTERS/SETTERS::PRIMITIVE TYPES ——————————————————————————————————————— #

	# Overwrite default DBCLass function for getting _id. This prevents it from being able to overwrite the value.
	def id(self) -> int:
		return self._id;


	def is_activated(self, *value: list) -> Union[bool, None]:
		if(len(value) == 0):
			return self._is_activated;

		if(not isinstance(value[0], bool)):
			raise Exception(f"is_activated must be of type '{bool.__name__}' not '{type(value[0]).__name__}'");
		self._is_activated = value[0];


	def length(self, *value: list) -> Union[int, None]:
		if(len(value) == 0):
			return self._length;

		if(not isinstance(value[0], int)):
			raise Exception(f"length must be of type '{int.__name__}' not '{type(value[0]).__name__}'");
		self._length = value[0];


	def moves_discretely(self, *value: list) -> Union[bool, None]:
		if(len(value) == 0):
			return self._moves_discretely;

		if(not isinstance(value[0], bool)):
			raise Exception(f"moves_discretely must be of type '{bool.__name__}' not '{type(value[0]).__name__}'");
		self._moves_discretely = value[0];


	def percentage(self, *value: list) -> Union[int, None]:
		if(len(value) == 0):
			return self._percentage;

		if(not isinstance(value[0], int)):
			raise Exception(f"percentage must be of type '{int.__name__}' not '{type(value[0]).__name__}'");
		self._percentage = value[0];


	# ——————————————————————————————————————————————— GETTERS: OBJECTS ——————————————————————————————————————————————— #

	def CurtainEvents(self) -> List["CurtainEvent"]:
		return self._CurtainEvents;


	# Gets the CurtainOption based on either name or id.
	# Takes a string or an int for the name of the CurtainOption.Option or the id of the CurtainOption.Option.id.
	def CurtainOption(self, **kwargs: dict) -> CurtainOption:
		return DBClass._exclusive_match(self._CurtainOptions, **kwargs);


	def CurtainOptions(self) -> List[CurtainOption]:
		return self._CurtainOptions;


	def SmartCurtain(self):
		return self._SmartCurtain;


	# ——————————————————————————————————————————————— GETTERS: SPECIAL ——————————————————————————————————————————————— #

	def CurtainEvent(self, **kwargs: dict) -> Union["CurtainEvent", None]:
		"""
		SUMMARY: Get CurtainsEvent if exists.
		PARAMS:  Takes the attribute name to match the event with.
		DETAILS: Checks whether the CurtainEvents exists in memory. If it doesn't, checks if it exists in the DB.
		RETURNS: Returns the Event if it is found, else None.
		"""
		from SmartCurtain.CurtainEvent import CurtainEvent;
		exclusive_match = DBClass._exclusive_match;

		if((curtain_event := exclusive_match(self._CurtainEvents, **kwargs)) is not None):
			return curtain_event;

		# Not found, check if in DB
		if((events := SELECT_CurtainsEvents_for_Curtains_id(self._id))):
			# If found in DB, create an object and add to the list
			if((event := exclusive_match([type("Temp", (), event)() for event in events], **kwargs)) is not None):
				curtain_event = CurtainEvent(**{**event, "Curtain": self});
				self._CurtainEvents.append(curtain_event);
				return curtain_event;

		return None;


	def CurtainEvents_for_range(self, *, latest: object=None, earliest: object=None) -> list:
		"""
		SUMMARY: Get all curtain events for a time range.
		PARAMS:  Takes the latest datetime time that an event can be, optionally the earliest datetime time an event can
		         be.
		DETAILS: Cycles through dictionary of events. If an event is within the range, event is added to list.
		RETURNS: A list of curtain events within that time range.
		"""
		if(not earliest and not latest):
			return self._CurtainEvents.copy();

		events = [];
		for event in self._CurtainEvents:
			if((latest and latest < event.time()) or (earliest and event.time() < earliest)):
				continue;
			events.append(event);
		return events;


	def buffer_time(self) -> int:
		return int(self._length / 6_400) + 2;


	def prior_CurtainEvents_for_current_day_of_week(self, earliest: object=None) -> list:
		earliest = earliest or datetime.today() - timedelta(days=28);

		#TODO: Get events for day of week.
		CurtainEvents_data = SELECT_CurtainsEvents();


	# ———————————————————————————————————————————————— EVENT CREATION ———————————————————————————————————————————————— #
	# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————

	def _new_event(self, percentage: int=0, *, Options_id: int=None, time: object=None) -> int:
		from SmartCurtain.CurtainEvent import CurtainEvent;

		if(time is None):
			time = datetime.now();

		kwargs = {"Curtain": self, "Options.id": Options_id, "percentage": percentage, "time": time};
		if((curtain_event_dict := CurtainEvent.add_event_to_DB(**kwargs)) is None):
			raise Exception("Unable to add event to DB");

		curtain_event: CurtainEvent = CurtainEvent(**{**curtain_event_dict, "Curtain": self});
		self._CurtainEvents.append(curtain_event);

		return curtain_event.id();


	def close(self, *, Options_id: int=None, time: datetime=None):
		if(time is None):
			time = datetime.now();

		return self._new_event(0, Options_id=Options_id, time=time);


	def open(self, percentage: int=100, *, Options_id: int=None, time: object=None) -> int:
		if(time is None):
			time = datetime.now();

		return self._new_event(percentage, Options_id=Options_id, time=time);
