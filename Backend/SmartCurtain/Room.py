#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2023.04.07                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import json
from paho import mqtt
import re
from typing import Optional, TypeVar


from SmartCurtain import Option
from SmartCurtain import AreaEvent
from SmartCurtain import AreaOption
from SmartCurtain import Curtain


Home = TypeVar("Home")
Room = TypeVar("Room")


class Room:
	def __init__(self, Home: Optional[Home]=None, *, id: int, is_deleted: bool, name: str,
	  RoomEvents: list[AreaEvent[Home]], RoomOptions: list[AreaOption[Room]], Curtains: list[Curtain]
	):
		# STRUCTURE #
		self._Home = Home
		# DATABASE #
		self._id: int = id
		self._is_deleted: bool = is_deleted
		self._name: str = name
		self._RoomEvents: list[AreaEvent[Room]] = RoomEvents.copy()
		self._RoomOptions: list[AreaOption[Room]] = RoomOptions.copy()
		self._Curtains: list[Curtain] = Curtains.copy()

		[room_event.Room(self) for room_event in self._RoomEvents]
		[room_event.start() for room_event in self._RoomEvents]
		[room_option.Room(self) for room_option in self._RoomOptions]
		[curtain.Room(self) for curtain in self._Curtains]


	@staticmethod
	def from_dictionary(room_data: dict) -> Room:
		events: list[AreaEvent[Room]] = []
		for event_data in room_data["RoomsEvents"]:
			event_data["Option"] = Option(**event_data["Option"]) if(event_data["Option"] is not None) else None
			events.append(AreaEvent.from_dictionary[Room](event_data))

		options: list = []
		for option_data in room_data["RoomsOptions"]:
			options.append(AreaOption[Room](**{**option_data, "Option": Option(**option_data["Option"])}))

		curtains: list[Curtain] = [Curtain.from_dictionary(curtain_data) for curtain_data in room_data["Curtains"]]

		return Room(id=room_data["id"], is_deleted=room_data["is_deleted"], name=room_data["name"], RoomEvents=events,
		  RoomOptions=options, Curtains=curtains)


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __delitem__(self, event: AreaEvent[Room]) -> None:
		self._RoomEvents.remove(event)


	def __getitem__(self, Curtain_id: int) -> Optional[Curtain]:
		return next((room for room in self._Curtains if(room.id() == Curtain_id)), None)


	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"is_deleted": self._is_deleted,
			"name": self._name,
			"RoomOptions": list(map(dict, self._RoomOptions)),
			"Curtains": list(map(dict, self._Curtains))
		}.items()


	def __repr__(self) -> str:
		return str(self)


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str, indent=4)


	def id(self):
		return self._id


	def is_deleted(self, new_is_deleted: Optional[bool]=None) -> Optional[bool]:
		if(new_is_deleted is None):
			return self._is_deleted

		if(not isinstance(new_is_deleted, bool)):
			raise Exception(f"'Room::is_deleted' must be of type 'bool' not '{type(new_is_deleted).__name__}'")

		self._is_deleted = new_is_deleted


	def name(self, new_name: Optional[str]=None) -> Optional[str]:
		if(new_name is None):
			return self._name

		if(not isinstance(new_name, str)):
			raise Exception(f"'Room::name' must be of type '{str.__name__}' not '{type(new_name).__name__}'")

		self._name = new_name


	# ————————————————————————————————————————— GETTERS & SETTERS::CHILDREN  ————————————————————————————————————————— #

	def Curtains(self):
		return self._Curtains.copy()


	def RoomEvents(self, *, Option_id: Optional[int]=None, is_activated: Optional[bool]=None,
	  is_deleted: Optional[bool]=None, percentage: Optional[int]=None
	) -> list[AreaEvent[Room]]:
		known_events: list[AreaEvent[Room]] = self._RoomEvents.copy()

		if(Option_id is not None):
			known_events = [event for event in known_events if(event.Option().id() == Option_id)]
		if(is_activated is not None):
			known_events = [event for event in known_events if(event.is_activated() == is_activated)]
		if(is_deleted is not None):
			known_events = [event for event in known_events if(event.is_deleted() == is_deleted)]
		if(percentage is not None):
			known_events = [event for event in known_events if(event.percentage() == percentage)]

		return known_events


	def RoomOption(self, identifier: int|str) -> Optional[AreaOption]:
		room_option = next((option for option in self._RoomOptions if(option == identifier)), None)
		if(room_option is not None):
			return room_option

		return self._Home.HomeOption(identifier)


	def RoomOptions(self) -> list[AreaOption[Room]]:
		return self._RoomOptions.copy()


	# —————————————————————————————————————————— GETTERS & SETTERS::PARENTS —————————————————————————————————————————— #

	def Home(self, new_Home: Optional[Home]=None) -> Optional[Home]:
		if(new_Home is None):
			return self._Home

		from SmartCurtain import Home
		if(not isinstance(new_Home, Home)):
			raise Exception(f"'Room::Home' must be of type 'Home' not '{type(new_Home).__name__}'")

		self._Home = new_Home


	# ————————————————————————————————————————————————————— MQTT ————————————————————————————————————————————————————— #

	def publish(self, command: str, payload: str) -> None:
		client = mqtt.client.Client()
		client.connect("localhost", 1883, 60)
		client.publish(f"SmartCurtain/-/{self._id}/{command}", payload)
