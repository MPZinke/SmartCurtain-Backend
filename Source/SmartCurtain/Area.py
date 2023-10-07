#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2023.06.04                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime
import json
from mpzinke import typename
from typing import Any, Optional, TypeVar


from SmartCurtain import DB


AreaEvent = TypeVar("AreaEvent")
AreaOption = TypeVar("AreaOption")


def wrong_type_string(instance: object, argument_name: str, required_type: type, supplied_value: Any) -> str:
	# "'{classname}::{argument_name}' must be of type '{required_type_name}' not '{supplied_type}'"
	message = "'{}::{}' must be of type '{}' not '{}'"
	return message.format(typename(instance), argument_name, required_type.__name__, typename(supplied_value))


class Area:
	def __init__(self, *, id: int, is_deleted: bool, name: str, AreaEvents: list[AreaEvent],
		AreaOptions: list[AreaOption]
	):
		self._id: int = id
		self.is_deleted: bool = is_deleted
		self.name: str = name

		self._AreaEvents = AreaEvents.copy()
		event_getter = property(type(self).AreaEvents_getter)
		setattr(type(self), f"AreaEvents", event_getter)  # EG `print(home.AreaEvents)`
		setattr(type(self), f"{typename(self)}Events", event_getter)  # EG `print(home.CurtainEvents)`
		setattr(type(self), f"_{typename(self)}Events", event_getter)  # EG `print(home._CurtainEvents)`

		self._AreaOptions = AreaOptions.copy()
		option_getter = property(type(self).AreaOptions_getter)
		setattr(type(self), f"AreaOptions", option_getter)  # EG `print(home.AreaOptions)`
		setattr(type(self), f"{typename(self)}Options", option_getter)  # EG `print(home.CurtainOptions)`
		setattr(type(self), f"_{typename(self)}Options", option_getter)  # EG `print(home._CurtainOptions)`

		for event in AreaEvents:
			event.Area = self
			event.start()

		for option in AreaOptions:
			option.Area = self


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __repr__(self) -> str:
		return str(self)


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str, indent=4)


	@property
	def id(self):
		return self._id


	@property
	def is_deleted(self, new_is_deleted: Optional[bool]=None) -> Optional[bool]:
		if(new_is_deleted is None):
			return self._is_deleted


	@is_deleted.setter
	def is_deleted(self, new_is_deleted: Optional[bool]=None) -> None:
		if(not isinstance(new_is_deleted, bool)):
			raise TypeError(wrong_type_string(self, "is_deleted", bool, new_is_deleted))

		self._is_deleted = new_is_deleted


	@property
	def name(self, new_name: Optional[str]=None) -> Optional[str]:
		if(new_name is None):
			return self._name


	@name.setter
	def name(self, new_name: Optional[str]=None) -> None:
		if(not isinstance(new_name, str)):
			raise TypeError(wrong_type_string(self, "new_name", str, new_name))

		self._name = new_name


	def AreaEvents_getter(self) -> list[AreaEvent]:
		return self._AreaEvents.copy()


	def AreaOptions_getter(self) -> list[AreaOption]:
		return self._AreaOptions.copy()


	# ———————————————————————————————————————————————————— EVENT  ———————————————————————————————————————————————————— #

	def new_AreaEvent(self, *, percentage: int, option: Optional[int], time: datetime) -> AreaEvent:
		from SmartCurtain import AreaEvent

		area = type(self)

		event_data = {f"{typename(self)}s.id": self._id, "Options.id": option, "percentage": percentage, "time": time}

		new_event_dict: dict = DB.DBFunctions.INSERT_Events[area](**event_data)
		new_event = AreaEvent[area](self, **new_event_dict)
		self._AreaEvents.append(new_event)
		new_event.start()

		return new_event
