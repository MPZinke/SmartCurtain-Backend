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


from typing import Dict, Optional


import SmartCurtain
from SmartCurtain.DB import DBFunctions
from Utility import wrong_type_string, LookupStruct


class Home(SmartCurtain.Area):
	def __init__(self, *, id: int, is_deleted: bool, name: str,
		HomeEvents: list[SmartCurtain.AreaEvent[SmartCurtain.Home]],
		HomeOptions: list[SmartCurtain.AreaOption[SmartCurtain.Home]], Rooms: list[SmartCurtain.Room]
	):
		SmartCurtain.Area.__init__(self, id=id, is_deleted=is_deleted, name=name, AreaEvents=HomeEvents,
			AreaOptions=HomeOptions
		)

		# STRUCTURE #
		self.Rooms: list[SmartCurtain.Room] = Rooms
		for room in self.Rooms:
			room.Home = self


	@staticmethod
	def all() -> list[SmartCurtain.Home]:
		return [Home.from_dictionary(home_data) for home_data in DBFunctions.SELECT_Homes()]


	@staticmethod
	def current() -> list[SmartCurtain.Home]:
		return [Home.from_dictionary(home_data) for home_data in DBFunctions.SELECT_Homes_WHERE_Current()]


	@staticmethod
	def from_dictionary(home_data: dict) -> SmartCurtain.Home:
		events: list[SmartCurtain.AreaEvent[SmartCurtain.Home]] = []
		for event_data in home_data["HomesEvents"]:
			event_data["Option"] = SmartCurtain.Option(**event_data["Option"]) if(event_data["Option"]) else None
			events.append(SmartCurtain.AreaEvent.from_dictionary[SmartCurtain.Home](event_data))

		options: list[SmartCurtain.AreaOption[SmartCurtain.Home]] = []
		for option_data in home_data["HomesOptions"]:
			option = SmartCurtain.Option(**option_data["Option"])
			options.append(SmartCurtain.AreaOption[SmartCurtain.Home](**{**option_data, "Option": option}))

		rooms: list[SmartCurtain.Room] = []
		for room_data in home_data["Rooms"]:
			rooms.append(SmartCurtain.Room.from_dictionary(room_data))

		return Home(id=home_data["id"], is_deleted=home_data["is_deleted"], name=home_data["name"], HomeEvents=events,
			HomeOptions=options, Rooms=rooms
		)


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __getitem__(self, Room_id: int|str) -> Optional[SmartCurtain.Room]|LookupStruct[SmartCurtain.Curtain]:
		"""
		RETURNS: If an int is supplied, the home with a matching ID is returned or none. If "-" is supplied, a
		         dictionary of the rooms and curtains is returned.
		         IE `{<curtain ids: curtains>}`
		"""
		return LookupStruct[SmartCurtain.Room, SmartCurtain.Curtain](self._Rooms)[Room_id]


	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"is_deleted": self._is_deleted,
			"name": self._name,
			"HomeEvents": list(map(dict, self._HomeEvents)),
			"HomeOptions": list(map(dict, self._HomeOptions)),
			"Rooms": list(map(dict, self._Rooms))
		}.items()


	def structure(self) -> Dict[str, SmartCurtain.Area]:
		return {
			"id": self.id
		}


	# ————————————————————————————————————————— GETTERS & SETTERS::CHILDREN  ————————————————————————————————————————— #

	@property
	def Rooms(self) -> list[SmartCurtain.Room]:
		return self._Rooms.copy()


	@Rooms.setter
	def Rooms(self, new_Rooms: list[SmartCurtain.Room]) -> None:
		if(any(not isinstance(room, SmartCurtain.Room) for room in new_Rooms)):
			raise TypeError(wrong_type_string(self, "Rooms", list[SmartCurtain.Room], []))

		self._Rooms = new_Rooms.copy()
