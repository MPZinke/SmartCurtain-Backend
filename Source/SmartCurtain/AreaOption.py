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
from mpzinke import typename, Generic
from typing import Any, Optional, TypeVar


Area = TypeVar("Home") | TypeVar("Room") | TypeVar("Curtain")
AreaOption = TypeVar("AreaOption")


def wrong_type_string(instance: object, argument_name: str, required_type: type, supplied_value: Any) -> str:
	# "'{classname}::{argument_name}' must be of type '{required_type_name}' not '{supplied_type}'"
	message = "'{}::{}' must be of type '{}' not '{}'"
	return message.format(typename(instance), argument_name, required_type.__name__, typename(supplied_value))


class AreaOption(Generic):
	def __init__(self, area: Optional[Area]=None, *, id: int, Option: object, data: Optional[dict|list],
	  is_deleted: bool, is_on: bool, notes: str
	):
		self._Area: Area = area
		# STRUCTURE #
		getter = property(type(self).Area_getter)
		setter = getter.setter(type(self).Area_setter)
		setattr(type(self), f"Area", getter)  # EG `print(event.Area)`
		setattr(type(self), f"Area", setter)  # EG `event.Area = curtain`
		setattr(type(self), self.__args__[0].__name__, getter)  # EG `print(event.Curtain)`
		setattr(type(self), self.__args__[0].__name__, setter)  # EG `event.Curtain = curtain`
		setattr(type(self), f"_{self.__args__[0].__name__}", getter)  # EG `print(event._Curtain)`
		setattr(type(self), f"_{self.__args__[0].__name__}", setter)  # EG `event._Curtain = curtain`

		# DATABASE #
		self._id: int = id
		self._Option: object = Option
		self._data: Optional[dict|list] = data
		self._is_deleted: bool = is_deleted
		self._is_on: bool = is_on
		self._notes: str = notes


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


	def Option(self):
		return self._Option


	def data(self, new_data: Optional[dict|list]=None) -> Optional[dict|list]:
		if(new_data is None):
			return self._data;

		if(not isinstance(new_data, dict|list)):
			value_type_str = type(new_data).__name__
			raise Exception(f"'Area::data' must be of type '{dict|list.__name__}' not '{value_type_str}'");

		self._data = new_data;


	def is_on(self, new_is_on: Optional[bool]=None) -> Optional[bool]:
		if(new_is_on is None):
			return self._is_on

		if(not isinstance(new_is_on, bool)):
			value_type_str = type(new_is_on).__is_on__
			raise Exception(f"'Area::is_on' must be of type 'bool' not '{value_type_str}'")

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
