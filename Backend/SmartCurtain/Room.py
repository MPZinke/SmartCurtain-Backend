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


from SmartCurtain import AreaOption;
from SmartCurtain import Curtain


Home = TypeVar("Home")
Room = TypeVar("Room")


class Room:
	def __init__(self, Home: Optional[Home]=None, *, id: int, is_deleted: bool, name: str,
	  RoomOptions: list[AreaOption[Room]], Curtains: list[Curtain]
	):
		# STRUCTURE #
		self._Home = Home
		# DATABASE #
		self._id: int = id
		self._is_deleted: bool = is_deleted
		self._name: str = name
		self._RoomOptions: list[AreaOption[Room]] = RoomOptions.copy()
		self._Curtains: list[Curtain] = Curtains.copy()

		[setattr(room_option, "_Room", self) for room_option in self._RoomOptions]
		[setattr(curtain, "_Room", self) for curtain in self._Curtains]


	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"is_deleted": self._is_deleted,
			"name": self._name,
			"RoomOptions": list(map(dict, self._RoomOptions)),
			"Curtains": list(map(dict, self._Curtains))
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


	def __getitem__(self, Curtain_id: int) -> Optional[Curtain]:
		return next((room for room in self._Curtains if(room.id() == Curtain_id)), None)


	def Curtains(self):
		return self._Curtains


def test():
	CurtainOptions = [AreaOption[Curtain](id=1, option=None, data={}, is_on=False, notes="Test")]
	Curtains = [
		Curtain(id=1, buffer_time=0, direction=None, is_deleted=False, length=None, name="Curtain", curtain_events=[],
		  CurtainOptions=CurtainOptions)
	]
	RoomOptions = [AreaOption[Room](id=2, option=None, data={}, is_on=False, notes="Test")]
	print(str(Room(id=1, is_deleted=False, name="Room", RoomOptions=RoomOptions, Curtains=Curtains)))


if(__name__ == "__main__"):
	test()
