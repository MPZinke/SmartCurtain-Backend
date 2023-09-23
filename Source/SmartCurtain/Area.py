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


from mpzinke import Generic
from typing import Optional, TypeVar


AreaEvent = TypeVar("AreaEvent")
AreaOption = TypeVar("AreaOption")


class Area(Generic):
	def __init__(self, *, id: int, is_deleted: bool, name: str, AreaEvents: list[AreaEvent],
	  AreaOptions: list[AreaOption]
	):
		self._id: int = id
		self._is_deleted: bool = is_deleted
		self._name: str = name
		self._AreaEvents: list[AreaEvent] = AreaEvents.copy()
		self._AreaOptions: list[AreaOption] = AreaOptions.copy()

		[event.Area(self) for event in self._AreaEvents]
		[event.start() for event in self._AreaEvents]
		[option.Area(self) for option in self._AreaOptions]


	def __repr__(self) -> str:
		return str(self)


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str, indent=4)


	def id(self):
		return self._id


	def is_deleted(self, new_is_deleted: Optional[bool]=None) -> Optional[bool]:
		if(new_is_deleted is None):
			return self._is_deleted

		if(not isinstance(new_is_deleted, bool)):
			raise Exception(f"'Home::is_deleted' must be of type 'bool' not '{type(new_is_deleted).__name__}'")

		self._is_deleted = new_is_deleted


	def name(self, new_name: Optional[str]=None) -> Optional[str]:
		if(new_name is None):
			return self._name

		if(not isinstance(new_name, str)):
			raise Exception(f"'Home::name' must be of type 'str' not '{type(new_is_deleted).__name__}'")

		self._name = new_name


	def AreaEvents(self, *, Option_id: Optional[int]=None, is_activated: Optional[bool]=None,
	  is_deleted: Optional[bool]=None, percentage: Optional[int]=None
	) -> list[AreaEvent]:
		known_events: list[AreaEvent] = self._AreaEvents.copy()

		if(Option_id is not None):
			known_events = [event for event in known_events if(event.Option().id() == Option_id)]
		if(is_activated is not None):
			known_events = [event for event in known_events if(event.is_activated() == is_activated)]
		if(is_deleted is not None):
			known_events = [event for event in known_events if(event.is_deleted() == is_deleted)]
		if(percentage is not None):
			known_events = [event for event in known_events if(event.percentage() == percentage)]

		return known_events


	def AreaOption(self, identifier: int|str) -> Optional[AreaOption]:
		return next((option for option in self._HomeOptions if(option == identifier)), None)
