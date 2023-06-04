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
from SmartCurtain import AreaOption
from SmartCurtain import AreaEvent
from SmartCurtain import Curtain
from SmartCurtain import Room
from SmartCurtain.DB import DBFunctions

from Utility import LookupStruct


Home = TypeVar("Home")


class Home:
	def __init__(self, *, id: int, is_deleted: bool, name: str, HomeEvents: list[AreaEvent[Home]],
	  HomeOptions: list[AreaOption[Home]], Rooms: list[Room]
	):
		self._id: int = id
		self._is_deleted: bool = is_deleted
		self._name: str = name
		self._HomeEvents: list[AreaEvent[Home]] = HomeEvents.copy()
		self._HomeOptions: list[AreaOption[Home]] = HomeOptions.copy()
		self._Rooms: list[Room] = Rooms.copy()

		[home_event.Home(self) for home_event in self._HomeEvents]
		[home_event.start() for home_event in self._HomeEvents]
		[home_option.Home(self) for home_option in self._HomeOptions]
		[room.Home(self) for room in self._Rooms]


	@staticmethod
	def all() -> list[Home]:
		return [Home.from_dictionary(home_data) for home_data in DBFunctions.SELECT_Homes()]


	@staticmethod
	def current() -> list[Home]:
		return [Home.from_dictionary(home_data) for home_data in DBFunctions.SELECT_Homes_WHERE_Current()]


	@staticmethod
	def current() -> list[Home]:
		return [Home.from_dictionary(home_data) for home_data in DBFunctions.SELECT_Homes_WHERE_Current()]


	@staticmethod
	def from_dictionary(home_data: dict) -> Home:
		events: list[AreaEvent[Home]] = []
		for event_data in home_data["HomesEvents"]:
			event_data["Option"] = Option(**event_data["Option"]) if(event_data["Option"] is not None) else None
			events.append(AreaEvent.from_dictionary[Home](event_data))

		options: list[AreaOption[Home]] = []
		for option_data in home_data["HomesOptions"]:
			options.append(AreaOption[Home](**{**option_data, "Option": Option(**option_data["Option"])}))

		rooms: list[Room] = [Room.from_dictionary(room_data) for room_data in home_data["Rooms"]]

		return Home(id=home_data["id"], is_deleted=home_data["is_deleted"], name=home_data["name"], HomeEvents=events,
		  HomeOptions=options, Rooms=rooms
		)


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __delitem__(self, event: AreaEvent[Home]) -> None:
		self._HomeEvents.remove(event)


	def __getitem__(self, Room_id: int|str) -> Optional[Room]|LookupStruct[Curtain]:
		"""
		RETURNS: If an int is supplied, the home with a matching ID is returned or none. If "-" is supplied, a
		         dictionary of the rooms and curtains is returned.
		         IE `{<curtain ids: curtains>}`
		"""
		return LookupStruct[Room, Curtain](self._Rooms)[Room_id]


	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"is_deleted": self._is_deleted,
			"name": self._name,
			"HomeOptions": list(map(dict, self._HomeOptions)),
			"Rooms": list(map(dict, self._Rooms))
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
			raise Exception(f"'Home::is_deleted' must be of type 'bool' not '{type(new_is_deleted).__name__}'")

		self._is_deleted = new_is_deleted


	def name(self, new_name: Optional[str]=None) -> Optional[str]:
		if(new_name is None):
			return self._name

		if(not isinstance(new_name, str)):
			raise Exception(f"'Home::name' must be of type 'str' not '{type(new_is_deleted).__name__}'")

		self._name = new_name


	# ————————————————————————————————————————— GETTERS & SETTERS::CHILDREN  ————————————————————————————————————————— #

	def Rooms(self):
		return self._Rooms.copy()


	def HomeEvents(self, *, Option_id: Optional[int]=None, is_activated: Optional[bool]=None,
	  is_deleted: Optional[bool]=None, percentage: Optional[int]=None
	) -> list[AreaEvent[Home]]:
		known_events: list[AreaEvent[Home]] = self._HomeEvents.copy()

		if(Option_id is not None):
			known_events = [event for event in known_events if(event.Option().id() == Option_id)]
		if(is_activated is not None):
			known_events = [event for event in known_events if(event.is_activated() == is_activated)]
		if(is_deleted is not None):
			known_events = [event for event in known_events if(event.is_deleted() == is_deleted)]
		if(percentage is not None):
			known_events = [event for event in known_events if(event.percentage() == percentage)]

		return known_events


	def HomeOption(self, identifier: int|str) -> Optional[AreaOption]:
		return next((option for option in self._HomeOptions if(option == identifier)), None)


	def HomeOptions(self) -> list[AreaOption[Home]]:
		return self._HomeOptions.copy()


	# ————————————————————————————————————————————————————— MQTT ————————————————————————————————————————————————————— #

	def publish(self, command: str, payload: str) -> None:
		client = mqtt.client.Client()
		client.connect("localhost", 1883, 60)
		client.publish(f"SmartCurtain/{self._id}/{command}", payload)
