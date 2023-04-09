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


import json;
from typing import Any, Generic, Optional, TypeVar, get_args


from Utility import Generic


Area = TypeVar("Area")


class AreaOption(Generic):
	def __init__(self, area: Optional[Area]=None, *, id: int, Option: object, data: Optional[dict|list], is_on: bool,
	  notes: str
	):
		# STRUCTURE #
		setattr(self, f"_{self.__args__[0].__name__}", area)
		setattr(self, self.__args__[0].__name__, self.get_or_set__args__)
		# DATABASE #
		self._id: int = id
		self._Option: object = Option
		self._data: Optional[dict|list] = data
		self._is_on: bool = is_on
		self._notes: bool = notes


	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"Option": dict(self._Option) if(self._Option is not None) else None,
			"data": self._data,
			"is_on": self._is_on,
			"notes": self._notes
		}.items();


	def __repr__(self) -> str:
		return str(self);


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str);


	def id(self):
		return self._id


	def get_or_set__args__(self, new__args__: Optional[Area]=None) -> Optional[Area]:
		__args___name = self.__args__[0].__name__
		if(new__args__ is None):
			return getattr(self, f"_{__args___name}")

		if(not isinstance(new__args__, self.__args__[0])):
			value_type_str = type(new__args__).__name__
			raise Exception(f"'__args__Option::{__args___name}' must be of type '{__args___name}' not '{value_type_str}'");

		setattr(self, f"_{__args___name}", new__args__)


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
			return self._is_on;

		if(not isinstance(new_is_on, bool)):
			value_type_str = type(new_is_on).__is_on__
			raise Exception(f"'Area::is_on' must be of type '{bool.__name__}' not '{value_type_str}'");

		self._is_on = new_is_on;


	def notes(self, new_notes: Optional[str]=None) -> Optional[str]:
		if(new_notes is None):
			return self._notes;

		if(not isinstance(new_notes, str)):
			value_type_str = type(new_notes).__notes__
			raise Exception(f"'Area::notes' must be of type '{str.__notes__}' not '{value_type_str}'");

		self._notes = new_notes;


def test():
	area_option = AreaOption[int](id=1, option=None, data=None, is_on=False, notes="Test")
	print(area_option.int())
	print(area_option.int(5))
	print(area_option.int())
	print(area_option.int("apples"))
	print(area_option.int())


if(__name__ == "__main__"):
	test()
