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
from mpzinke import typename
from paho import mqtt
import re
from typing import Any, Dict, Optional, TypeVar


from SmartCurtain import Option
from SmartCurtain import Area
from SmartCurtain import AreaEvent
from SmartCurtain import AreaOption
from SmartCurtain import Curtain
from Utility import wrong_type_string


Home = type("Home", (), {})
Room = type("Room", (), {})


class Room(Area):
	def __init__(self, Home: Optional[Home]=None, *, id: int, is_deleted: bool, name: str,
		RoomEvents: list[AreaEvent[Home]], RoomOptions: list[AreaOption[Room]], Curtains: list[Curtain]
	):
		Area.__init__(self, id=id, is_deleted=is_deleted, name=name, AreaEvents=RoomEvents, AreaOptions=RoomOptions)
		# STRUCTURE #
		self.Home = Home
		self.Curtains: list[Curtain] = Curtains

		for curtain in self.Curtains:
			curtain.Room = self


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
			RoomOptions=options, Curtains=curtains
		)


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __delitem__(self, event: AreaEvent[Room]) -> None:
		self._RoomEvents.remove(event)


	def __getitem__(self, Curtain_id: int) -> Optional[Curtain]:
		return next((room for room in self._Curtains if(room.id == Curtain_id)), None)


	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"is_deleted": self._is_deleted,
			"name": self._name,
			"RoomEvents": list(map(dict, self._RoomEvents)),
			"RoomOptions": list(map(dict, self._RoomOptions)),
			"Curtains": list(map(dict, self._Curtains))
		}.items()


	# ————————————————————————————————————————— GETTERS & SETTERS::CHILDREN  ————————————————————————————————————————— #

	@property
	def Curtains(self):
		return self._Curtains.copy()


	@Curtains.setter
	def Curtains(self, new_Curtains: list[Curtain]) -> None:
		if(any(not isinstance(curtain, Curtain) for curtain in new_Curtains)):
			raise TypeError(wrong_type_string(self, "Curtains", list[Curtain], []))

		self._Curtains = new_Curtains.copy()


	def structure(self) -> Dict[str, Area]:
		return {
			"id": self._id,
			"Home.id": self._Room.Home().id
		}


	# —————————————————————————————————————————— GETTERS & SETTERS::PARENTS —————————————————————————————————————————— #

	@property
	def Home(self) -> Optional[Home]:
		return self._Home


	@Home.setter
	def Home(self, new_Home: Home) -> None:
		from SmartCurtain import Home

		if(not isinstance(new_Home, Optional[Home])):
			raise TypeError(wrong_type_string(self, "Home", Home, new_Home))

		self._Home = new_Home
