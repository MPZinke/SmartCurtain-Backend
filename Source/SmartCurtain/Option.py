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


import json


import SmartCurtain
from SmartCurtain.DB import DBFunctions
from Utility import wrong_type_string


class Option:
	def __init__(self, *, id: int, description: str, is_deleted: bool, name: str):
		assert(isinstance(id, int)), wrong_type_string(self, "id", int, id)
		self._id: int = id
		self.description: str = description
		self.is_deleted: bool = is_deleted
		self.name: str = name


	def __eq__(self, right: int|str) -> bool:
		if(isinstance(right, str)):
			return self._name == right
		elif(isinstance(right, int)):
			return self._id == right

		raise NotImplementedError()


	@staticmethod
	def all() -> list[SmartCurtain.Option]:
		return [Option(**option_data) for option_data in DBFunctions.SELECT_Options()]


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

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


	# ———————————————————————————————————————— GETTERS & SETTERS::ATTRIBUTES  ———————————————————————————————————————— #

	def id(self):
		return self._id


	@property
	def description(self) -> str:
		return self._description


	@description.setter
	def description(self, new_description: str) -> None:
		if(not isinstance(new_description, str)):
			raise TypeError(wrong_type_string(self, "description", str, new_description))

		self._description = new_description


	@property
	def is_deleted(self) -> bool:
		return self._is_deleted


	@is_deleted.setter
	def is_deleted(self, new_is_deleted: bool) -> None:
		if(not isinstance(new_is_deleted, bool)):
			raise TypeError(wrong_type_string(self, "is_deleted", bool, new_is_deleted))

		self._is_deleted = new_is_deleted


	@property
	def name(self) -> str:
		return self._name


	@name.setter
	def name(self, new_name: str) -> None:
		if(not isinstance(new_name, str)):
			raise TypeError(wrong_type_string(self, "name", str, new_name))

		self._name = new_name
