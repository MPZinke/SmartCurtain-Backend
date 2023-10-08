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


import SmartCurtain
from Utility import wrong_type_string


class AreaOption(Generic):
	def __init_subclass__(cls):
		getter = property(cls.Area_getter)
		setter = getter.setter(cls.Area_setter)
		setattr(cls, "Area", getter)  # EG `print(option.Area)`
		setattr(cls, "Area", setter)  # EG `option.Area = curtain`
		setattr(cls, cls.__args__[0].__name__, getter)  # EG `print(option.Curtain)`
		setattr(cls, cls.__args__[0].__name__, setter)  # EG `option.Curtain = curtain`


	def __init__(self, Area: Optional[SmartCurtain.Area]=None, *, id: int, Option: SmartCurtain.Option,
		data: Optional[dict|list], is_deleted: bool, is_on: bool, notes: str
	):
		# STRUCTURE #
		self.Area: Area = Area
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


	def Area_getter(self) -> Optional[SmartCurtain.Area]:
		return self._Area


	def Area_setter(self, new_Area: Optional[SmartCurtain.Area]) -> None:
		if(not isinstance(new_Area, Optional[self.__args__[0]])):
			raise TypeError(wrong_type_string(self, "Area", self.__args__[0], new_Area))

		self._Area = new_Area


	@property
	def Option(self) -> SmartCurtain.Option:
		return self._Option


	@Option.setter
	def Option(self, new_Option: SmartCurtain.Option) -> None:
		if(not isinstance(new_Option, SmartCurtain.Option)):
			raise TypeError(wrong_type_string(self, "Option", SmartCurtain.Option, new_Option))

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
	def is_on(self) -> bool:
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
			raise TypeError(wrong_type_string(self, "notes", str, new_notes))

		self._notes = new_notes
