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
import re
from typing import Optional, TypeVar


from SmartCurtain import Option
from SmartCurtain import AreaOption
from SmartCurtain import AreaEvent
from SmartCurtain import Curtain
from SmartCurtain import Room
from SmartCurtain.DB import DBFunctions


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
		[home_option.Home(self) for home_option in self._HomeOptions]
		[room.Home(self) for room in self._Rooms]


	@staticmethod
	def all() -> list[Home]:
		return [Home.from_dictionary(home_data) for home_data in DBFunctions.SELECT_Homes()]


	@staticmethod
	def current() -> list[Home]:
		return [Home.from_dictionary(home_data) for home_data in DBFunctions.SELECT_Homes_WHERE_Current()]


	@staticmethod
	def from_dictionary(home_data: dict) -> Home:
		events: list[AreaEvent[Home]] = []
		for event_data in home_data["HomesEvents"]:
			# Flatten the tables
			event = event_data["Event"]
			event_data = {"id": event_data["id"], "is_deleted": event_data["is_deleted"], "Event.id": event["id"], 
			  "is_activated": event["is_activated"], "percentage": event["percentage"], "time": event["time"],
			  "Option": Option(**event["Option"]) if(event["Option"] is not None) else None
			}
			events.append(AreaEvent.from_dictionary[Home](**event_data))

		options: list[AreaOption[Home]] = []
		for option_data in home_data["HomesOptions"]:
			options.append(AreaOption[Home](**{**option_data, "Option": Option(**option_data["Option"])}))

		rooms: list[Room] = [Room.from_dictionary(room_data) for room_data in home_data["Rooms"]]

		return Home(id=home_data["id"], is_deleted=home_data["is_deleted"], name=home_data["name"], HomeEvents=events,
		  HomeOptions=options, Rooms=rooms
		)


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __getitem__(self, Room_id: int) -> Optional[Room]:
		return next((room for room in self._Rooms if(room.id() == Room_id)), None)


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


	def HomeOption(self, Option_id: int) -> Optional[AreaOption[Home]]:
		return next((option for option in self._HomeOptions if(option.Option().id() == Option_id)), None)


	def HomeOptions(self) -> list[AreaOption[Home]]:
		return self._HomeOptions.copy()


	# ————————————————————————————————————————— GETTERS & SETTERS::CHILDREN  ————————————————————————————————————————— #

	def Rooms(self):
		return self._Rooms.copy()


	# ————————————————————————————————————————————————————— MQTT ————————————————————————————————————————————————————— #

	def path(self) -> str:
		path_name = re.sub(r"[^_\-a-zA-Z0-9]", "", self._name)
		return f"SmartCurtain/{path_name}"
