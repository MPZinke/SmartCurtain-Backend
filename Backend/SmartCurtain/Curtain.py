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


from datetime import datetime, timedelta
import json
import os
import re
import requests
from typing import List, Optional, TypeVar, Union


from SmartCurtain import Option
from SmartCurtain import AreaOption
from SmartCurtain import CurtainEvent


Curtain = TypeVar("Curtain")
Room = TypeVar("Room")


class Curtain:
	def __init__(self, Room: Optional[Room]=None, *, id: int, buffer_time: int, direction: Optional[bool],
	  is_deleted: bool, length: Optional[int], name: str, CurtainEvents: list[CurtainEvent],
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
		self._CurtainEvents: list[CurtainEvent] = CurtainEvents.copy()
		self._CurtainOptions: list[AreaOption[Curtain]] = CurtainOptions.copy()
		# TEMP STATE #
		self._is_moving: bool = False
		self._percentage: int = 0

		[curtain_event.Curtain(self) for curtain_event in self._CurtainOptions]
		[curtain_option.Curtain(self) for curtain_option in self._CurtainOptions]


	@staticmethod
	def from_dictionary(curtain_data: dict) -> Curtain:
		events: list[CurtainEvents] = []
		for event in curtain_data["CurtainsEvents"]:
			# print("Event", event)
			pass

		options: list[CurtainOptions] = []
		for option_data in curtain_data["CurtainsOptions"]:
			options.append(AreaOption[Curtain](**{**option_data, "Option": Option(**option_data["Option"])}))

		return Curtain(id=curtain_data["id"], buffer_time=curtain_data["buffer_time"],
		   direction=curtain_data["direction"], is_deleted=curtain_data["is_deleted"], length=curtain_data["length"],
		   name=curtain_data["name"], CurtainEvents=events, CurtainOptions=options
		)


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __getitem__(self, curtain_event_id: int) -> Optional[CurtainEvent]:
		return next((event for event in self._CurtainEvents if(event.id() == curtain_event_id)), None)


	def __iter__(self) -> dict:
		yield from {
			# DATABASE #
			"id": self._id,
			"buffer_time": self._buffer_time,
			"direction": self._direction,
			"is_deleted": self._is_deleted,
			"length": self._length,
			"name": self._name,
			"CurtainEvents": list(map(dict, self._CurtainEvents)),
			"CurtainOptions": list(map(dict, self._CurtainOptions)),
			# TEMP STATE #
			"is_moving": self._is_moving,
			"percentage": self._percentage
		}.items()


	def __repr__(self) -> str:
		return str(self)


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str, indent=4)


	def id(self):
		return self._id


	def buffer_time(self, new_buffer_time: Optional[int]=None) -> Optional[int]:
		if(new_buffer_time is None):
			return self._buffer_time

		if(not isinstance(new_buffer_time, int)):
			raise Exception(f"'Curtain::buffer_time' must be of type 'int' not '{type(new_buffer_time).__name__}'")

		self._buffer_time = new_buffer_time


	def is_deleted(self, new_is_deleted: Optional[int]=None) -> Optional[int]:
		if(new_is_deleted is None):
			return self._is_deleted

		if(not isinstance(new_is_deleted, int)):
			raise Exception(f"'Curtain::is_deleted' must be of type 'bool' not '{type(new_is_deleted).__name__}'")

		self._is_deleted = new_is_deleted


	def is_moving(self, new_is_moving: Optional[bool]=None) -> Optional[bool]:
		if(new_is_moving is None):
			return self._is_moving

		if(not isinstance(new_is_moving, bool)):
			raise Exception(f"'Curtain::is_moving' must be of type 'bool' not '{type(new_is_moving).__name__}'")

		self._is_moving = new_is_moving


	def length(self, new_length: Optional[int]=None) -> Optional[int]:
		if(new_length is None):
			return self._length

		if(not isinstance(new_length, int)):
			raise Exception(f"'Curtain::length' must be of type 'int' not '{type(new_length).__name__}'")

		self._length = new_length


	def percentage(self, new_percentage: Optional[int]=None) -> Optional[int]:
		if(new_percentage is None):
			return self._percentage

		if(not isinstance(new_percentage, int)):
			raise Exception(f"'Curtain::percentage' must be of type 'int' not '{type(new_percentage).__name__}'")

		self._percentage = new_percentage


	def CurtainOption(self, Option_id: int) -> Optional[AreaOption[Host]]:
		return next((option for option in self._CurtainOptions if(option.Option().id() == Option_id)), None)


	def CurtainOptions(self) -> list[AreaOption[Curtain]]:
		return self._CurtainOptions.copy()


	# ————————————————————————————————————————— GETTERS & SETTERS::CHILDREN  ————————————————————————————————————————— #

	def CurtainEvent(self, *, id: Optional[int]=None, time: Optional[datetime]=None) -> Optional[CurtainEvent]:
		if(id is not None):
			if((event := next((event for event in self._CurtainEvents if(event.id() == id)), None)) is not None):
				return event

		if(time is not None):
			if((event := next((event for event in self._CurtainEvents if(event.time() == time)), None)) is not None):
				return event

		return None


	def CurtainEvents(self, *, Option_id: Optional[int]=None, is_activated: Optional[bool]=None,
	  is_deleted: Optional[bool]=None, percentage: Optional[int]=None
	) -> list[CurtainEvent]:
		known_events: list[CurtainEvent] = self._CurtainEvents.copy()

		if(Option_id is not None):
			known_events = [event for event in known_events if(event.Option().id() == Option_id)]
		if(is_activated is not None):
			known_events = [event for event in known_events if(event.is_activated() == is_activated)]
		if(is_deleted is not None):
			known_events = [event for event in known_events if(event.is_deleted() == is_deleted)]
		if(percentage is not None):
			known_events = [event for event in known_events if(event.percentage() == percentage)]

		return known_events


	# —————————————————————————————————————————— GETTERS & SETTERS::PARENTS —————————————————————————————————————————— #

	def Room(self, new_Room: Optional[int]=None) -> Optional[int]:
		if(new_Room is None):
			return self._Room

		if(not isinstance(new_Room, int)):
			raise Exception(f"'Curtain::Room' must be of type 'int' not '{type(new_Room).__name__}'")

		self._Room = new_Room


	# ————————————————————————————————————————————————————— MQTT ————————————————————————————————————————————————————— #

	def path(self) -> str:
		path_name = re.sub(r"[^_\-a-zA-Z0-9]", "", self._name)
		return f"{self._Room.path()}/{path_name}"


	def publish(self, payload: str) -> None:
		client = MQTTClient()
		client.connect("localhost", 1883, 60)
		client.publish(self.path(), payload)
