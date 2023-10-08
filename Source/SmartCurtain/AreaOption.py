#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.29                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import json
from mpzinke import Generic
from typing import Optional, TypeVar


from SmartCurtain import Option
from Utility import wrong_type_string


Area = TypeVar("Home") | TypeVar("Room") | TypeVar("Curtain")
AreaOption = TypeVar("AreaOption")


class AreaOption(Generic):
	def __init__(self, area: Optional[Area]=None, *, id: int, Option: object, data: Optional[dict|list],
	  is_deleted: bool, is_on: bool, notes: str
	):
		# STRUCTURE #
		self._Area: Area = area

		getter = property(type(self).Area_getter)
		setter = getter.setter(type(self).Area_setter)
		setattr(type(self), f"Area", getter)  # EG `print(event.Area)`
		setattr(type(self), f"Area", setter)  # EG `event.Area = curtain`
		setattr(type(self), self.__args__[0].__name__, getter)  # EG `print(event.Curtain)`
		setattr(type(self), self.__args__[0].__name__, setter)  # EG `event.Curtain = curtain`
		# DATABASE #
		assert(isinstance(id, int)), wrong_type_string(self, "id", int, id)
		self._id: int = id
		self.Option: object = Option
		self.data: Optional[dict|list] = data
		self.is_deleted: bool = is_deleted
		self.is_on: bool = is_on
		self.notes: str = notes


	def __eq__(self, right: int|str) -> bool:
		return self._Option == right


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"Option": dict(self._Option) if(self._Option is not None) else None,
			"data": self._data,
			"is_on": self._is_on,
			"notes": self._notes
		}.items()


	def __repr__(self) -> str:
		return str(self)


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str)


	# ———————————————————————————————————————— GETTERS & SETTERS::ATTRIBUTES  ———————————————————————————————————————— #

	def id(self):
		return self._id


	def Area_getter(self) -> Optional[Area]:
		return self._Area


	def Area_setter(self, new_Area) -> None:
		if(not isinstance(new_Area, self.__args__[0])):
			raise TypeError(wrong_type_string(self, "Area", self.__args__[0], new_Area))

		self._Area = new_Area


	@property
	def Option(self) -> Option:
		return self._Option


	@Option.setter
	def Option(self, new_Option: Option) -> None:
		if(not isinstance(new_Option, Option)):
			raise TypeError(wrong_type_string(self, "Option", Option, new_Option))

		self._Option = new_Option


	@property
	def data(self=None) -> Optional[dict|list]:
		return self._data;


	@data.setter
	def data(self, new_data: Optional[dict|list]) -> None:
		if(not isinstance(new_data, Optional[dict|list])):
			raise TypeError(wrong_type_string(self, "data", Optional[dict|list], new_data))

		self._data = new_data


	@property
	def is_on(self) -> Optional[bool]:
		return self._is_on


	@is_on.setter
	def is_on(self, new_is_on: Optional[bool]=None) -> None:
		if(not isinstance(new_is_on, bool)):
			raise TypeError(wrong_type_string(self, "is_on", bool, new_is_on))

		self._is_on = new_is_on


	@property
	def notes(self) -> str:
		return self._notes


	@notes.setter
	def notes(self, new_notes: str) -> None:
		if(not isinstance(new_notes, str)):
			value_type_str = type(new_notes).__notes__
			raise Exception(f"'Area::notes' must be of type 'str' not '{value_type_str}'")

		self._notes = new_notes
