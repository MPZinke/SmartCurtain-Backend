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
from typing import Dict, Optional


import SmartCurtain
from SmartCurtain import DB
from Utility import wrong_type_string


class Area:
	def __init_subclass__(cls):
		event_getter = property(cls.AreaEvents_getter)
		event_setter = event_getter.setter(cls.AreaEvents_setter)
		cls.AreaEvents = event_setter
		setattr(cls, "AreaEvents", event_setter)  # EG `print(home.AreaEvents)`
		setattr(cls, f"{cls.__name__}Events", event_setter)  # EG `print(home.CurtainEvents)`
		setattr(cls, f"_{cls.__name__}Events", event_setter)  # EG `print(self._CurtainEvents)`

		setattr(cls, f"{cls.__name__}Events", cls.new_AreaEvent)  # EG `curtain.new_CurtainEvent`

		option_getter = property(cls.AreaOptions_getter)
		option_setter = option_getter.setter(cls.AreaOptions_setter)
		cls.AreaOptions = option_setter
		setattr(cls, "AreaOptions", option_setter)  # EG `print(home.AreaOptions)`
		setattr(cls, f"{cls.__name__}Options", option_setter)  # EG `print(home.CurtainOptions)`
		setattr(cls, f"_{cls.__name__}Options", option_setter)  # EG `print(self._CurtainOptions)`


	def __init__(self, *, id: int, is_deleted: bool, name: str, AreaEvents: list[SmartCurtain.AreaEvent],
		AreaOptions: list[SmartCurtain.AreaOption]
	):
		# STRUCTURE #
		self.AreaEvents: SmartCurtain.AreaEvent = AreaEvents
		for event in AreaEvents:
			event.Area = self
			event.start()

		self.AreaOptions: SmartCurtain.AreaOption = AreaOptions
		for option in AreaOptions:
			option.Area = self
		# DATABASE #
		assert(isinstance(id, int)), wrong_type_string(self, "id", int, id)
		self._id: int = id
		self.is_deleted: bool = is_deleted
		self.name: str = name

		setattr(self, f"{type(self).__name__}Option", self.AreaOption)


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __delitem__(self, event_id: int) -> None:
		if((event := next((event for event in self.AreaEvents if(event.id == event_id)), None)) is None):
			raise KeyError(f"No event with id '{event_id}' found for {self.__args__[0].__name__} with id '{self.id}'")

		self._AreaEvents.remove(event)  # `self._AreaEvents` so that the event is removed from the saved list
		event.__del__()


	def __repr__(self) -> str:
		return str(self)


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str, indent=4)


	@property
	def id(self):
		return self._id


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
			raise TypeError(wrong_type_string(self, "new_name", str, new_name))

		self._name = new_name


	def structure(self) -> Dict[str, SmartCurtain.Area]:
		raise NotImplementedError("Structure must be specified on the inherited class")


	def AreaEvents_getter(self) -> list[SmartCurtain.AreaEvent]:
		return self._AreaEvents.copy()


	def AreaEvents_setter(self, new_AreaEvents: list[SmartCurtain.AreaEvent]) -> None:
		for area_event in new_AreaEvents:
			if(not isinstance(area_event, SmartCurtain.AreaEvent) or area_event.__args__ != (type(self),)):
				raise TypeError(wrong_type_string(self, "AreaEvents", list[SmartCurtain.AreaEvent], area_event))

		self._AreaEvents = new_AreaEvents.copy()


	def AreaOptions_getter(self) -> list[SmartCurtain.AreaOption]:
		return self._AreaOptions.copy()


	def AreaOptions_setter(self, new_AreaOptions: list[SmartCurtain.AreaOption]) -> None:
		for area_option in new_AreaOptions:
			if(not isinstance(area_option, SmartCurtain.AreaOption) or area_option.__args__ != (type(self),)):
				raise TypeError(wrong_type_string(self, "AreaOptions", list[SmartCurtain.AreaOption], area_option))

		self._AreaOptions = new_AreaOptions.copy()


	def AreaOption(self, identifier: int|str) -> Optional[SmartCurtain.AreaOption]:
		area_options: list[SmartCurtain.AreaOption] = getattr(self, f"_{type(self).__name__}Options")
		return next((option for option in area_options if(option == identifier)), None)


	# ———————————————————————————————————————————————————— EVENT  ———————————————————————————————————————————————————— #

	def new_AreaEvent(self, *, percentage: int, option: Optional[int], time: datetime) -> SmartCurtain.AreaEvent:
		event_data = {f"{typename(self)}s.id": self._id, "Options.id": option, "percentage": percentage, "time": time}

		new_event_dict: dict = DB.DBFunctions.INSERT_Events[type(self)](**event_data)
		new_event = SmartCurtain.AreaEvent[type(self)](self, **new_event_dict)
		self._AreaEvents.append(new_event)  # `self._AreaEvents` so that the event is removed from the saved list

		new_event.start()

		return new_event
