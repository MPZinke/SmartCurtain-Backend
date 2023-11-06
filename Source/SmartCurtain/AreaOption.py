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


from bson.objectid import ObjectId
import json
from mpzinke import Generic
from typing import Any, Optional


import SmartCurtain
from SmartCurtain import DB
from Utility import wrong_type_string


class AreaOption(Generic):
	def __init_subclass__(cls):
		getter = property(cls.Area_getter)
		setter = getter.setter(cls.Area_setter)
		setattr(cls, "Area", getter)  # EG `print(option.Area)`
		setattr(cls, "Area", setter)  # EG `option.Area = curtain`
		setattr(cls, cls.__args__[0].__name__, getter)  # EG `print(option.Curtain)`
		setattr(cls, cls.__args__[0].__name__, setter)  # EG `option.Curtain = curtain`


	def __init__(self, Area: Optional[SmartCurtain.Area]=None, *, Option: SmartCurtain.Option,
		data: Optional[dict|list], is_enabled: bool, notes: str
	):
		# STRUCTURE #
		self.Area: Area = Area
		# DATABASE #
		self.Option: SmartCurtain.Option = Option
		self.data: Optional[dict|list] = data
		self.is_enabled: bool = is_enabled
		self.notes: str = notes


	@Generic
	def from_dictionary(__args__, area_option_data: dict) -> SmartCurtain.AreaOption:
		area_option_data = area_option_data.copy()
		if(f"{__args__[0].__name__}s.id" in area_option_data):
			del area_option_data[f"{__args__[0].__name__}s.id"]

		if("Options.id" in area_option_data):
			del area_option_data["Options.id"]

		if(isinstance(area_option_data["Option"], dict)):
			area_option_data["Option"] = SmartCurtain.Option(area_option_data["Option"])

		return AreaOption[__args__[0]](**area_option_data)


	def __eq__(self, right: int|str) -> bool:
		return self._Option == right


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __iter__(self) -> dict:
		yield from {
			"Option": dict(self._Option) if(self._Option is not None) else None,
			"data": self._data,
			"is_enabled": self._is_enabled,
			"notes": self._notes
		}.items()


	def __repr__(self) -> str:
		return str(self)


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str)


	# ———————————————————————————————————————— GETTERS & SETTERS::ATTRIBUTES  ———————————————————————————————————————— #

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
	def data(self=None) -> Optional[Any]:
		return self._data;


	@data.setter
	def data(self, new_data: Optional[Any]) -> None:
		self._data = new_data


	@property
	def is_enabled(self) -> bool:
		return self._is_enabled


	@is_enabled.setter
	def is_enabled(self, new_is_enabled: Optional[bool]=None) -> None:
		if(not isinstance(new_is_enabled, bool)):
			raise TypeError(wrong_type_string(self, "is_enabled", bool, new_is_enabled))

		self._is_enabled = new_is_enabled


	@property
	def notes(self) -> str:
		return self._notes


	@notes.setter
	def notes(self, new_notes: str) -> None:
		if(not isinstance(new_notes, str)):
			raise TypeError(wrong_type_string(self, "notes", str, new_notes))

		self._notes = new_notes
