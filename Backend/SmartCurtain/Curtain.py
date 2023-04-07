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
import json;
import os;
import requests;
from typing import List, Optional, TypeVar, Union;


from SmartCurtain import AreaOption;
from SmartCurtain import CurtainEvent;


Curtain = TypeVar("Curtain")
Room = TypeVar("Room")


class Curtain:
	def __init__(self, Room: Optional[Room]=None, *, id: int, buffer_time: int, direction: Optional[bool],
	  is_deleted: bool, length: Optional[int], name: str, curtain_events: list[CurtainEvent],
	  CurtainOptions: list[AreaOption[Curtain]]
	):
		# STRUCTURE #
		self._Room = Room
		# DATABASE #
		self._id: int = id
		self._buffer_time: int = buffer_time
		self._direction: Optional[bool] = direction
		self._is_deleted: bool = is_deleted
		self._length: Optional[int] = length
		self._name: str = name
		self._curtain_events: list[CurtainEvent] = curtain_events.copy()
		self._CurtainOptions: list[AreaOption[Curtain]] = CurtainOptions.copy()
		# TEMP STATE #
		self._is_moving: bool = False
		self._percentage: int = 0

		[setattr(curtain_option, "_Curtain", self) for curtain_option in self._CurtainOptions]


	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"buffer_time": self._buffer_time,
			"direction": self._direction,
			"is_deleted": self._is_deleted,
			"length": self._length,
			"name": self._name,
			"curtain_events": list(map(dict, self._curtain_events)),
			"CurtainOptions": list(map(dict, self._CurtainOptions)),
			"is_moving": self._is_moving,
			"percentage": self._percentage
		}.items();


	def __repr__(self) -> str:
		return str(self);


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str);


	def path(self) -> str:
		path_name = re.sub(r"[^_\-a-zA-Z0-9]", "", self._name)
		return f"{self._room.path()}/Curtain-{path_name}"


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


	def is_moving(self, new_is_moving: Optional[bool]=None) -> Optional[bool]:
		if(new_is_moving is None):
			return self._is_moving;

		if(not isinstance(new_is_moving, bool)):
			raise Exception(f"'is_moving' must be of type '{bool.__name__}' not '{type(new_is_moving).__name__}'");

		self._is_moving = new_is_moving;


	def length(self, new_length: Optional[int]=None) -> Optional[int]:
		if(new_length is None):
			return self._length;

		if(not isinstance(new_length, int)):
			raise Exception(f"'length' must be of type '{int.__name__}' not '{type(new_length).__name__}'");

		self._length = new_length;


	def percentage(self, new_percentage: Optional[int]=None) -> Optional[int]:
		if(new_percentage is None):
			return self._percentage;

		if(not isinstance(new_percentage, int)):
			raise Exception(f"'percentage' must be of type '{int.__name__}' not '{type(new_percentage).__name__}'");

		self._percentage = new_percentage;


	# ——————————————————————————————————————————————— GETTERS: OBJECTS ——————————————————————————————————————————————— #

	def __getitem__(self, curtain_event_id: int) -> Optional[CurtainEvent]:
		return next((event for event in self._curtain_events if(event.id() == curtain_event_id)), None)


	def CurtainEvents(self) -> List["CurtainEvent"]:
		return self._CurtainEvents;


	# Gets the CurtainOption based on either name or id.
	# Takes a string or an int for the name of the CurtainOption.Option or the id of the CurtainOption.Option.id.
	def CurtainOption(self, **kwargs: dict) -> AreaOption[Curtain]:
		return DBClass._exclusive_match(self._CurtainOptions, **kwargs);


	def CurtainOptions(self) -> list[AreaOption[Curtain]]:
		return self._CurtainOptions;


	def Room(self):
		return self._Room;


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


def test():
	CurtainOptions = [AreaOption[Curtain](id=1, option=None, data={}, is_on=False, notes="Test")]
	print(str(Curtain(id=1, buffer_time=0, direction=None, is_deleted=False, length=None, name="Curtain",
	  curtain_events=[], CurtainOptions=CurtainOptions)))


if(__name__ == "__main__"):
	test()
