#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.10.14                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import sys


Option = type("Option", (), {})
AreaEvent = type("AreaEvent", (), {})
AreaOption = type("AreaOption", (), {})
Area = type("Area", (), {})
Curtain = type("Curtain", (), {})
Room = type("Room", (), {})
Home = type("Home", (), {})
setattr(sys.modules[__name__], "SmartCurtain", type("SmartCurtain", (), {}))


from SmartCurtain import DB
from SmartCurtain.Option import Option
from SmartCurtain.AreaEvent import AreaEvent
from SmartCurtain.AreaOption import AreaOption
from SmartCurtain.Area import Area
from SmartCurtain.Curtain import Curtain
from SmartCurtain.Room import Room
from SmartCurtain.Home import Home


# ————————————————————————————————————————————— SMARTCURTAIN DECLARATION ————————————————————————————————————————————— #

import json
from typing import Optional


from Utility import wrong_type_string, LookupStruct


class SmartCurtain:
	def __init__(self):
		self.current()


	# ——————————————————————————————————————————————— GETTERS/SETTERS  ——————————————————————————————————————————————— #

	def __iter__(self) -> dict:
		yield from {
			"Homes": [dict(home) for home in self.Homes],
			"Options": [dict(option) for option in self.Options]
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str)


	def __getitem__(self, Home_id: int|str) -> Optional[Home]|LookupStruct[Room, Curtain]:
		"""
		RETURNS: If an int is supplied, the home with a matching ID is returned or none. If "-" is supplied, a...
		"""
		return LookupStruct[Home, Room, Curtain](self.Homes)[Home_id]


	@property
	def Homes(self) -> list[Home]:
		return self._Homes.copy()


	@Homes.setter
	def Homes(self, new_Homes: list[Home]) -> None:
		for home in new_Homes:
			if(not isinstance(home, Home)):
				raise TypeError(wrong_type_string(self, "Homes", list[Home], home))

		self._Homes = new_Homes.copy()


	def Room(self, Room_id: int) -> Optional[Room]:
		return self["-"][Room_id]


	@property
	def Rooms(self) -> list[Room]:
		return list(self["-"])


	def Curtain(self, Curtain_id: int) -> Optional[Curtain]:
		return self["-"]["-"][Curtain_id]


	@property
	def Curtains(self) -> list[Room]:
		return list(self["-"]["-"])


	@property
	def Options(self) -> list[Option]:
		return self._Options.copy()


	@Options.setter
	def Options(self, new_Options: list[Option]) -> None:
		for option in new_Options:
			if(not isinstance(option, Option)):
				raise TypeError(wrong_type_string(self, "Options", list[Option], option))

		self._Options = new_Options.copy()



	def current(self) -> None:
		self.Options = Option.all()
		options = self.Options

		curtains = list(DB.SMART_CURTAIN_DATABASE.Curtains.find())
		curtains_events = list(DB.SMART_CURTAIN_DATABASE.CurtainsEvents.find())
		for curtain in curtains:
			curtain["CurtainsEvents"] = list(filter(lambda event: event["_id"] in curtain["CurtainsEvents"], curtains_events))

			for curtain_option in curtain["CurtainsOptions"]:
				curtain_option["Option"] = next(option for option in options if(option.id == curtain_option["Option"]))

		rooms = list(DB.SMART_CURTAIN_DATABASE.Rooms.find())
		rooms_events = list(DB.SMART_CURTAIN_DATABASE.RoomsEvents.find())
		for room in rooms:
			room["RoomsEvents"] = list(filter(lambda event: event["_id"] in room["RoomsEvents"], rooms_events))
			room["Curtains"] = list(filter(lambda event: event["_id"] in room["Curtains"], curtains))

			for rooms_option in room["RoomsOptions"]:
				rooms_option["Option"] = next(option for option in options if(option.id == rooms_option["Option"]))

		homes = list(DB.SMART_CURTAIN_DATABASE.Homes.find())
		homes_events = list(DB.SMART_CURTAIN_DATABASE.HomesEvents.find())
		for home in homes:
			home["HomesEvents"] = list(filter(lambda event: event["_id"] in home["HomesEvents"], homes_events))
			home["Rooms"] = list(filter(lambda event: event["_id"] in home["Rooms"], rooms))

			for homes_option in home["HomesOptions"]:
				homes_option["Option"] = next(option for option in options if(option.id == homes_option["Option"]))

		self.Homes = [Home.from_dictionary(home_dict) for home_dict in homes]
		for home in self.Homes:
			home.SmartCurtain = self


	def resync(self) -> None:
		for area in [self.Homes, self.Rooms, self.Curtains]:
			for event in area.AreaEvents:
				del area[event.id]

		self.Homes = Home.current()
		for home in self.Homes:
			home.SmartCurtain = self
		self.Options = Option.all()
