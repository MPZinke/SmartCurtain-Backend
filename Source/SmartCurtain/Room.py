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
from Utility import wrong_type_string


class Room(SmartCurtain.Area):
	def __init__(self, Home: Optional[SmartCurtain.Home]=None, *, id: int, is_deleted: bool, name: str,
		RoomEvents: list[SmartCurtain.AreaEvent[SmartCurtain.Room]],
		RoomOptions: list[SmartCurtain.AreaOption[SmartCurtain.Room]],
		Curtains: list[SmartCurtain.Curtain]
	):
		SmartCurtain.Area.__init__(self, id=id, is_deleted=is_deleted, name=name, AreaEvents=RoomEvents,
			AreaOptions=RoomOptions
		)
		# STRUCTURE #
		self.Home: SmartCurtain.Home = Home
		self.Curtains: list[SmartCurtain.Curtain] = Curtains
		for curtain in self.Curtains:
			curtain.Room = self


	@staticmethod
	def from_dictionary(room_data: dict) -> SmartCurtain.Room:
		events: list[SmartCurtain.AreaEvent[SmartCurtain.Room]] = []
		for event_data in room_data["RoomsEvents"]:
			event_data["Option"] = SmartCurtain.Option(**event_data["Option"]) if(event_data["Option"]) else None
			events.append(SmartCurtain.AreaEvent.from_dictionary[SmartCurtain.Room](event_data))

		options: list = []
		for option_data in room_data["RoomsOptions"]:
			option = SmartCurtain.Option(**option_data["Option"])
			options.append(SmartCurtain.AreaOption[SmartCurtain.Room](**{**option_data, "Option": option}))

		curtains: list[SmartCurtain.Curtain] = []
		for curtain_data in room_data["Curtains"]:
			curtains.append(SmartCurtain.Curtain.from_dictionary(curtain_data))

		return Room(id=room_data["id"], is_deleted=room_data["is_deleted"], name=room_data["name"], RoomEvents=events,
			RoomOptions=options, Curtains=curtains
		)


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __getitem__(self, Curtain_id: int) -> Optional[SmartCurtain.Curtain]:
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
	def Curtains(self) -> list[SmartCurtain.Curtain]:
		return self._Curtains.copy()


	@Curtains.setter
	def Curtains(self, new_Curtains: list[SmartCurtain.Curtain]) -> None:
		if(any(not isinstance(curtain, SmartCurtain.Curtain) for curtain in new_Curtains)):
			raise TypeError(wrong_type_string(self, "Curtains", list[SmartCurtain.Curtain], []))

		self._Curtains = new_Curtains.copy()


	def structure(self) -> Dict[str, SmartCurtain.Area]:
		return {
			"id": self._id,
			"Home.id": self.Home.id
		}


	# —————————————————————————————————————————— GETTERS & SETTERS::PARENTS —————————————————————————————————————————— #

	@property
	def Home(self) -> Optional[SmartCurtain.Home]:
		return self._Home


	@Home.setter
	def Home(self, new_Home: Home) -> None:
		if(not isinstance(new_Home, Optional[SmartCurtain.Home])):
			raise TypeError(wrong_type_string(self, "Home", SmartCurtain.Home, new_Home))

		self._Home = new_Home
