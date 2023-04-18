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


from datetime import datetime, timedelta
import json
from requests import post
from typing import Optional, TypeVar
from warnings import warn as Warn


from SmartCurtain import DB
from SmartCurtain import Option
from Utility import Generic
from Utility.ZThread import ZThreadSingle
from Utility import Logger


Area = TypeVar("Area")
AreaEvent = TypeVar("AreaEvent")
Option = TypeVar("Option")


class AreaEvent(Generic):
	def __init__(self, area: Optional[Area]=None, *, id: int, Option: Optional[object], is_activated: bool,
	  is_deleted: bool, percentage: int, time: datetime, **kwargs: dict
	):
		# STRUCTURE #
		setattr(self, f"_{self.__args__[0].__name__}", area)
		setattr(self, self.__args__[0].__name__, self.get_or_set__args__)
		# DATABASE #
		self._id: int = id
		self._is_activated: bool = is_activated
		self._is_deleted: bool = is_deleted
		self._Option: Optional[object] = Option
		self._percentage: int = percentage
		self._time: datetime = time
		# THREAD #
		# if(not self._is_activated and not self._is_deleted and datetime.now() < self._time):
		self._publish_thread = ZThreadSingle(f"Event Thread #{self._id}", self.publish, self.sleep_time)
		self._publish_thread.start()


	@Generic
	def from_dictionary(__args__: set, curtain_event_data: dict) -> AreaEvent:
		option = Option(**curtain_event_data["Option"]) if(curtain_event_data["Option"] is not None) else None
		return AreaEvent[__args__[0]](**{**curtain_event_data, "Option": option})


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"is_activated": self._is_activated,
			"is_deleted": self._is_deleted,
			"percentage": self._percentage,
			"Option": dict(self._Option) if(self._Option is not None) else None,
			"time": self._time
		}.items()


	def __repr__(self) -> str:
		return str(self)


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str, indent=4)


	# ———————————————————————————————————————— GETTERS & SETTERS::ATTRIBUTES  ———————————————————————————————————————— #

	def id(self):
		return self._id


	def is_activated(self, new_is_activated: Optional[bool]=None) -> Optional[bool]:
		if(new_is_activated is None):
			return self._is_activated

		if(not isinstance(new_is_activated, bool)):
			message = f"'AreaEvent[{self.__args__[0]}]::is_activated' must be of type 'bool' not '{type(new_is_activated).__name__}'"
			raise Exception(message)

		self._is_activated = new_is_activated


	def is_deleted(self, new_is_deleted: Optional[bool]=None) -> Optional[bool]:
		if(new_is_deleted is None):
			return self._is_deleted

		if(not isinstance(new_is_deleted, bool)):
			raise Exception(f"'AreaEvent[{self.__args__[0]}]::is_deleted' must be of type 'bool' not '{type(new_is_deleted).__name__}'")

		self._is_deleted = new_is_deleted


	def percentage(self, new_percentage: Optional[int]=None) -> Optional[int]:
		if(new_percentage is None):
			return self._percentage

		if(not isinstance(new_percentage, int)):
			raise Exception(f"'AreaEvent[{self.__args__[0]}]::percentage' must be of type 'int' not '{type(new_percentage).__name__}'")

		self._percentage = new_percentage


	def Option(self, new_Option: Optional[Option]=None) -> Optional[Option]:
		if(new_Option is None):
			return self._Option

		if(not isinstance(new_Option, Option)):
			raise Exception(f"'AreaEvent[{self.__args__[0]}]::Option' must be of type 'Option' not '{type(new_Option).__name__}'")

		self._Option = new_Option


	def time(self, new_time: Optional[datetime]=None) -> Optional[datetime]:
		if(new_time is None):
			return self._time

		if(not isinstance(new_time, datetime)):
			raise Exception(f"'AreaEvent[{self.__args__[0]}]::time' must be of type 'datetime' not '{type(new_time).__name__}'")

		self._time = new_time


	# ——————————————————————————————————————————————————— PUBLISH  ——————————————————————————————————————————————————— #

	def publish(self) -> None:
		print("Beep Boop")
		payload = {"type": "move", "event": {"id": self._id, "percentage": self._percentage}}
		self._Curtain.publish(json.dumps(payload))
		DB.DBFunctions.UPDATE_Events[self.__args__[0]](self._id, is_activated=True)


	def sleep_time(self):
		if((now := datetime.now()) > self._time + timedelta(seconds=1)):
			Warn(f"Event {self._id} is scheduled at a time in the past")

		return (self._time - now).seconds if(now < self._time) else .25
