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


from bson.objectid import ObjectId
import json
from typing import Optional


import SmartCurtain
from SmartCurtain import DB
from Utility import wrong_type_string


class Option:
	def __init__(self, *, _id: ObjectId, description: str, name: str):
		assert(isinstance(_id, ObjectId)), wrong_type_string(self, "_id", ObjectId, _id)
		self._id: ObjectId = _id
		self.description: str = description
		self.name: str = name


	def __eq__(self, right: int|str) -> bool:
		if(right is None):
			return False

		elif(isinstance(right, str)):
			return self.name == right

		elif(isinstance(right, int)):
			return self.id == right

		raise NotImplementedError()


	@staticmethod
	def all() -> list[SmartCurtain.Option]:
		return [Option(**option_data) for option_data in list(SmartCurtain.DB.SMART_CURTAIN_DATABASE.Options.find())]


	@staticmethod
	def from_id(id: int) -> SmartCurtain.Option:
		option_data: Optional[dict] = DB.Option_by_id(id)
		if(option_data is None):
			raise ValueError(f"No Option with id '{id}' found")

		return SmartCurtain.Option(**option_data)


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"description,": self._description,
			"name": self._name
		}.items()


	def __repr__(self) -> str:
		return str(self)


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str)


	# ———————————————————————————————————————— GETTERS & SETTERS::ATTRIBUTES  ———————————————————————————————————————— #

	@property
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
	def name(self) -> str:
		return self._name


	@name.setter
	def name(self, new_name: str) -> None:
		if(not isinstance(new_name, str)):
			raise TypeError(wrong_type_string(self, "name", str, new_name))

		self._name = new_name
