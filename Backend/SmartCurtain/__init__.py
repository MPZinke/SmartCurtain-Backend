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


import json
from typing import Optional


from SmartCurtain.Option import Option
from SmartCurtain.AreaEvent import AreaEvent
from SmartCurtain.AreaOption import AreaOption
from SmartCurtain.Curtain import Curtain
from SmartCurtain.Room import Room
from SmartCurtain.Home import Home


class SmartCurtain:
	def __init__(self):
		self._Homes: list[Home] = Home.current()
		self._Options: list[Option] = Option.all()


	# ——————————————————————————————————————————————— GETTERS/SETTERS  ——————————————————————————————————————————————— #

	def __iter__(self) -> dict:
		yield from {
			"Homes": [dict(home) for home in self._Homes],
			"Options": [dict(option) for option in self._Options]
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str)



	def __getitem__(self, Home_id: int) -> Optional[Home]:
		if(Home_id == "-"):
			room_dict = {room.id(): room for home in self._Homes for room in home.Rooms()}
			curtain_dict = {curtain.id(): curtain for room in room_dict.values() for curtain in room.Curtains()}
			return {**room_dict, "-": curtain_dict}

		return next((home for home in self._Homes if(home.id() == Home_id)), None)


	def Homes(self) -> list[Home]:
		return self._Homes.copy()


	def Room(self, Room_id: int) -> Optional[Room]:
		for home in self._Homes:
			if((room := home[Room_id]) is not None):
				return room

		return None


	def Curtain(self, Curtain_id: int) -> Optional[Curtain]:
		for home in self._Homes:
			for room in home.Rooms():
				if((curtain := room[Curtain_id]) is not None):
					return curtain

		return None
