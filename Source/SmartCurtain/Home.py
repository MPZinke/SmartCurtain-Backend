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


from bson.objectid import ObjectId
import json
from typing import Dict, Optional


import SmartCurtain
from Utility import wrong_type_string, LookupStruct


class Home(SmartCurtain.Area):
	def __init__(self, *, _id: ObjectId, name: str, HomeEvents: list[SmartCurtain.AreaEvent[SmartCurtain.Home]],
		HomeOptions: list[SmartCurtain.AreaOption[SmartCurtain.Home]], Rooms: list[SmartCurtain.Room]
	):
		SmartCurtain.Area.__init__(self, _id=_id, name=name, AreaEvents=HomeEvents, AreaOptions=HomeOptions)

		# STRUCTURE #
		self.Rooms: list[SmartCurtain.Room] = Rooms
		for room in self.Rooms:
			room.Home = self


	@staticmethod
	def from_dictionary(home_data: dict) -> SmartCurtain.Home:
		events: list[SmartCurtain.AreaEvent[SmartCurtain.Home]] = []
		for event_data in home_data["HomesEvents"]:
			events.append(SmartCurtain.AreaEvent.from_dictionary[SmartCurtain.Home](event_data))

		options: list[SmartCurtain.AreaOption[SmartCurtain.Home]] = []
		for option_data in home_data["HomesOptions"]:
			options.append(SmartCurtain.AreaOption.from_dictionary[SmartCurtain.Home](option_data))

		rooms: list[SmartCurtain.Room] = []
		for room_data in home_data["Rooms"]:
			rooms.append(SmartCurtain.Room.from_dictionary(room_data))

		return Home(_id=home_data["_id"], name=home_data["name"], HomeEvents=events, HomeOptions=options, Rooms=rooms)


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
			"name": self.name,
			"HomeEvents": list(map(dict, self.HomeEvents)),
			"HomeOptions": list(map(dict, self.HomeOptions)),
			"Rooms": list(map(dict, self.Rooms))
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


	@property
	def SmartCurtain(self) -> SmartCurtain.SmartCurtain:
		return self._SmartCurtain


	@SmartCurtain.setter
	def SmartCurtain(self, smart_curtain: Optional[object]) -> None:
		if(not isinstance(smart_curtain, SmartCurtain.SmartCurtain)):
			raise TypeError(wrong_type_string(self, "SmartCurtain", SmartCurtain.SmartCurtain, smart_curtain))

		self._SmartCurtain = smart_curtain
