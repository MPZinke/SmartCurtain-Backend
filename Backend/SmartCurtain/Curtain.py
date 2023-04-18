#!/opt/homebrew/bin/python3
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
from paho.mqtt.client import Client as MQTTClient
import re
import requests
from typing import List, Optional, TypeVar, Union


from SmartCurtain import AreaEvent
from SmartCurtain import AreaOption
from SmartCurtain import Option


Curtain = TypeVar("Curtain")
Room = TypeVar("Room")


class Curtain:
	def __init__(self, Room: Optional[Room]=None, *, id: int, direction: Optional[bool],
	  is_deleted: bool, length: Optional[int], name: str, CurtainEvents: list[AreaEvent[Curtain]],
	  CurtainOptions: list[AreaOption[Curtain]]
	):
		# STRUCTURE #
		self._Room = Room
		# DATABASE #
		self._id: int = id
		self._direction: Optional[bool] = direction
		self._is_deleted: bool = is_deleted
		self._length: Optional[int] = length
		self._name: str = name
		self._CurtainEvents: list[AreaEvent[Curtain]] = CurtainEvents.copy()
		self._CurtainOptions: list[AreaOption[Curtain]] = CurtainOptions.copy()
		# TEMP STATE #
		self._is_connected: bool = False
		self._is_moving: bool = False
		self._percentage: int = 0

		[curtain_event.Curtain(self) for curtain_event in self._CurtainEvents]
		[curtain_option.Curtain(self) for curtain_option in self._CurtainOptions]


	@staticmethod
	def from_dictionary(curtain_data: dict) -> Curtain:
		events: list[AreaEvent[Home]] = []
		for event_data in curtain_data["CurtainsEvents"]:
			# Flatten the tables
			event = event_data["Event"]
			event_data = {"id": event_data["id"], "is_deleted": event_data["is_deleted"], "Event.id": event["id"], 
			  "is_activated": event["is_activated"], "percentage": event["percentage"], "time": event["time"],
			  "Option": Option(**event["Option"]) if(event["Option"] is not None) else None
			}
			events.append(AreaEvent.from_dictionary[Curtain](event_data))

		options: list[CurtainOptions] = []
		for option_data in curtain_data["CurtainsOptions"]:
			options.append(AreaOption[Curtain](**{**option_data, "Option": Option(**option_data["Option"])}))

		return Curtain(id=curtain_data["id"], direction=curtain_data["direction"],
		  is_deleted=curtain_data["is_deleted"], length=curtain_data["length"], name=curtain_data["name"],
		  CurtainEvents=events, CurtainOptions=options
		)


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __getitem__(self, curtain_event_id: int) -> Optional[AreaEvent[Curtain]]:
		return next((event for event in self._CurtainEvents if(event.id() == curtain_event_id)), None)


	def __iter__(self) -> dict:
		yield from {
			# DATABASE #
			"id": self._id,
			"direction": self._direction,
			"is_deleted": self._is_deleted,
			"length": self._length,
			"name": self._name,
			"CurtainEvents": list(map(dict, self._CurtainEvents)),
			"CurtainOptions": list(map(dict, self._CurtainOptions)),
			# TEMP STATE #
			"is_connected": self._is_connected,
			"is_moving": self._is_moving,
			"percentage": self._percentage
		}.items()


	def __repr__(self) -> str:
		return str(self)


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str, indent=4)


	def node_dict(self) -> dict:
		node_dict = {
			"id": self._id,
			"Room.id": self._Room.id(),
			"Home.id": self._Room.Home().id()
		}

		if(self._direction is not None):
			node_dict["direction"] = self._direction
		if(self._length is not None):
			node_dict["length"] = self._length

		if((option := self.CurtainOption("Auto Calibrate")) is not None):
			node_dict["Auto Calibrate"] = option.is_on()
		if((option := self.CurtainOption("Auto Correct")) is not None):
			node_dict["Auto Correct"] = option.is_on()


	# ———————————————————————————————————————— GETTERS & SETTERS::ATTRIBUTES  ———————————————————————————————————————— #

	def id(self):
		return self._id


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


	def is_connected(self, new_is_connected: Optional[bool]=None) -> Optional[bool]:
		if(new_is_connected is None):
			return self._is_connected

		if(not isinstance(new_is_connected, bool)):
			raise Exception(f"'Curtain::is_connected' must be of type 'bool' not '{type(new_is_connected).__name__}'")

		self._is_connected = new_is_connected


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


	# ————————————————————————————————————————— GETTERS & SETTERS::CHILDREN  ————————————————————————————————————————— #

	def CurtainEvents(self, *, Option_id: Optional[int]=None, is_activated: Optional[bool]=None,
	  is_deleted: Optional[bool]=None, percentage: Optional[int]=None
	) -> list[AreaEvent[Curtain]]:
		known_events: list[AreaEvent[Curtain]] = self._CurtainEvents.copy()

		if(Option_id is not None):
			known_events = [event for event in known_events if(event.Option().id() == Option_id)]
		if(is_activated is not None):
			known_events = [event for event in known_events if(event.is_activated() == is_activated)]
		if(is_deleted is not None):
			known_events = [event for event in known_events if(event.is_deleted() == is_deleted)]
		if(percentage is not None):
			known_events = [event for event in known_events if(event.percentage() == percentage)]

		return known_events


	def CurtainOption(self, identifier: int|str) -> Optional[AreaOption]:
		curtain_option = next((option for option in self._CurtainOptions if(option == identifier)), None)
		if(curtain_option is not None):
			return curtain_option

		return self._Room.RoomOption(identifier)


	def CurtainOptions(self) -> list[AreaOption[Curtain]]:
		return self._CurtainOptions.copy()


	# —————————————————————————————————————————— GETTERS & SETTERS::PARENTS —————————————————————————————————————————— #

	def Room(self, new_Room: Optional[Room]=None) -> Optional[Room]:
		if(new_Room is None):
			return self._Room

		from SmartCurtain import Room
		if(not isinstance(new_Room, Room)):
			raise Exception(f"'Curtain::Room' must be of type 'Room' not '{type(new_Room).__name__}'")

		self._Room = new_Room


	# ————————————————————————————————————————————————————— MQTT ————————————————————————————————————————————————————— #

	def path(self) -> str:
		path_name = re.sub(r"[^_\-a-zA-Z0-9]", "", self._name)
		return f"{self._Room.path()}/{path_name}"


	def publish(self, payload: str) -> None:
		client = MQTTClient()
		client.connect("localhost", 1883, 60)
		client.publish(self.path(), payload)
