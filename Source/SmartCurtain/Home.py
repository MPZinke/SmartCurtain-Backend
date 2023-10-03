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
from SmartCurtain import Area
from SmartCurtain import AreaOption
from SmartCurtain import AreaEvent
from SmartCurtain import Curtain
from SmartCurtain import Room
from SmartCurtain.DB import DBFunctions

from Utility import LookupStruct


Home = type("Home", (), {})


class Home(Area):
	def __init__(self, *, id: int, is_deleted: bool, name: str, HomeEvents: list[AreaEvent[Home]],
		HomeOptions: list[AreaOption[Home]], Rooms: list[Room]
	):
		Area.__init__(self, id=id, is_deleted=is_deleted, name=name, AreaEvents=HomeEvents, AreaOptions=HomeOptions)

		# STRUCTURE #
		self._Rooms: list[Room] = Rooms.copy()

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
			"HomeEvents": list(map(dict, self._HomeEvents)),
			"HomeOptions": list(map(dict, self._HomeOptions)),
			"Rooms": list(map(dict, self._Rooms))
		}.items()


	# ————————————————————————————————————————— GETTERS & SETTERS::CHILDREN  ————————————————————————————————————————— #

	def Rooms(self):
		return self._Rooms.copy()
