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
from mpzinke import Generic
from typing import Optional, TypeVar


from SmartCurtain import DB


AreaEvent = TypeVar("AreaEvent")
AreaOption = TypeVar("AreaOption")


class Area:
	def __init__(self, *, id: int, is_deleted: bool, name: str, AreaEvents: list[AreaEvent],
		AreaOptions: list[AreaOption]
	):
		self._id: int = id
		self._is_deleted: bool = is_deleted
		self._name: str = name
		# Set attributes
		setattr(self, f"_{type(self).__name__}Events", AreaEvents.copy())
		setattr(self, f"_{type(self).__name__}Options", AreaOptions.copy())

		# Set methods
		setattr(self, f"{type(self).__name__}Events", self.AreaEvents)
		setattr(self, f"{type(self).__name__}Option", self.AreaOption)
		setattr(self, f"{type(self).__name__}Options", self.AreaOptions)
		setattr(self, f"new_{type(self).__name__}Event", self.new_AreaEvent)

		[event.Area(self) for event in AreaEvents]
		[event.start() for event in AreaEvents]
		[option.Area(self) for option in AreaOptions]


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
			raise Exception(f"'Home::name' must be of type 'str' not '{type(new_name).__name__}'")

		self._name = new_name


	def AreaEvents(self, *, Option_id: Optional[int]=None, is_activated: Optional[bool]=None,
		is_deleted: Optional[bool]=None, percentage: Optional[int]=None
	) -> list[AreaEvent]:
		area_events: list[AreaEvent] = getattr(self, f"_{type(self).__name__}Events")
		known_events: list[AreaEvent] = area_events.copy()

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
		area_options: list[AreaOption] = getattr(self, f"_{type(self).__name__}Options")
		return next((option for option in area_options if(option == identifier)), None)


	def AreaOptions(self) -> list[AreaOption]:
		return getattr(self, f"_{type(self).__name__}Options").copy()


	def new_AreaEvent(self, *, percentage: int, option: Optional[int], time: datetime) -> AreaEvent:
		from SmartCurtain import AreaEvent

		area = type(self)
		if(time < datetime.now()):
			raise ValueError(f"""'{time.strftime("%Y-%m-%d %H:%M:%S")}' is too far in the past""")

		event_data = {f"{area.__name__}s.id": self._id, "Options.id": option, "percentage": percentage, "time": time}

		new_event_dict: dict = DB.DBFunctions.INSERT_Events[type(self)](**event_data)
		new_event = AreaEvent[area](self, **new_event_dict)
		getattr(self, f"_{area.__name__}Events").append(new_event)
		new_event.start()

		return new_event
