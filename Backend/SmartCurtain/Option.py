#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.23                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from typing import Optional


class Option:
	def __init__(self, id: int, description: str, is_deleted: bool, name: str):
		self._id: int = id
		self._description: str = description
		self._is_deleted: bool = is_deleted
		self._name: str = name


	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"description,": self._description,
			"is_deleted": self._is_deleted,
			"name": self._name
		}.items()


	def __repr__(self) -> str:
		return str(self)


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str)


	def id(self):
		return self._id


	def description(self, new_description: Optional[int]=None) -> Optional[int]:
		if(new_description is None):
			return self._description

		if(not isinstance(new_description, int)):
			value_type_str = type(new_description).__name__
			raise Exception(f"'Home::description' must be of type '{int.__name__}' not '{value_type_str}'")

		self._description = new_description


	def is_deleted(self, new_is_deleted: Optional[int]=None) -> Optional[int]:
		if(new_is_deleted is None):
			return self._is_deleted

		if(not isinstance(new_is_deleted, int)):
			value_type_str = type(new_is_deleted).__name__
			raise Exception(f"'Home::is_deleted' must be of type '{int.__name__}' not '{value_type_str}'")

		self._is_deleted = new_is_deleted


	def name(self, new_name: Optional[int]=None) -> Optional[int]:
		if(new_name is None):
			return self._name

		if(not isinstance(new_name, int)):
			value_type_str = type(new_name).__name__
			raise Exception(f"'Home::name' must be of type '{int.__name__}' not '{value_type_str}'")

		self._name = new_name


	def Rooms(self):
		return self._Rooms


