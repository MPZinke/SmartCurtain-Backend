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
from typing import Optional, TypeVar


from SmartCurtain import AreaOption
from SmartCurtain import Curtain
from SmartCurtain import Room


Home = TypeVar("Home")


class Home:
	def __init__(self, *, id: int, is_deleted: bool, name: str, HomeOptions: list[AreaOption[Home]], Rooms: list[Room]):
		self._id: int = id
		self._is_deleted: bool = is_deleted
		self._name: str = name
		self._HomeOptions: list[AreaOption[Home]] = HomeOptions.copy()
		self._Rooms: list[Room] = Rooms.copy()

		[setattr(home_option, "_Home", self) for home_option in self._HomeOptions]
		[setattr(room, "_Home", self) for room in self._Rooms]


	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"is_deleted": self._is_deleted,
			"name": self._name,
			"HomeOptions": list(map(dict, self._HomeOptions)),
			"Rooms": list(map(dict, self._Rooms))
		}.items();


	def __repr__(self) -> str:
		return str(self);


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str);


	def path(self) -> str:
		path_name = re.sub(r"[^_\-a-zA-Z0-9]", "", self._name)
		return f"SmartCurtain/{path_name}"



	def id(self):
		return self._id


	def is_deleted(self, new_is_deleted: Optional[int]=None) -> Optional[int]:
		if(new_is_deleted is None):
			return self._is_deleted;

		if(not isinstance(new_is_deleted, int)):
			value_type_str = type(new_is_deleted).__name__
			raise Exception(f"'Home::is_deleted' must be of type '{int.__name__}' not '{value_type_str}'");

		self._is_deleted = new_is_deleted;


	def name(self, new_name: Optional[int]=None) -> Optional[int]:
		if(new_name is None):
			return self._name;

		if(not isinstance(new_name, int)):
			value_type_str = type(new_name).__name__
			raise Exception(f"'Home::name' must be of type '{int.__name__}' not '{value_type_str}'");

		self._name = new_name;


	def __getitem__(self, Room_id: int) -> Optional[Room]:
		return next((room for room in self._Rooms if(room.id() == Room_id)), None)


	def Rooms(self):
		return self._Rooms


def test():
	CurtainOptions = [AreaOption[Curtain](id=1, option=None, data={}, is_on=False, notes="Test")]
	Curtains = [
		Curtain(id=1, buffer_time=0, direction=None, is_deleted=False, length=None, name="Curtain", curtain_events=[],
		  CurtainOptions=CurtainOptions)
	]
	RoomOptions = [AreaOption[Room](id=2, option=None, data={}, is_on=False, notes="Test")]
	Rooms = [Room(id=1, is_deleted=False, name="Room", RoomOptions=RoomOptions, Curtains=Curtains)]
	HomeOptions = [AreaOption[Home](id=3, option=None, data={}, is_on=False, notes="Test")]
	print(str(Home(id=1, is_deleted=False, name="Home", HomeOptions=HomeOptions, Rooms=Rooms)))



if(__name__ == "__main__"):
	test()
