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
from mpzinke import threading, Generic
from paho import mqtt
from typing import Optional, TypeVar
from warnings import warn as Warn


import SmartCurtain
from SmartCurtain import Area
from SmartCurtain import DB
from SmartCurtain import Option


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
		self._publish_thread = threading.DelayThread(f"Event Thread #{self._id}", action=self, time=self.sleep_time)


	@Generic
	def from_dictionary(__args__: set, curtain_event_data: dict) -> AreaEvent:
		option = Option(**curtain_event_data["Option"]) if(curtain_event_data["Option"] is not None) else None
		return AreaEvent[__args__[0]](**{**curtain_event_data, "Option": option})


	def __del__(self) -> None:
		try:
			self._publish_thread.kill()
		except:
			pass


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __eq__(self, right) -> bool:
		return self._id == right.id()


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


	def get_or_set__args__(self, new_Area: Optional[Area]=None) -> Optional[Area]:
		area_type = self.__args__[0]
		area_type_name = area_type.__name__
		if(new_Area is None):
			return getattr(self, f"_{area_type_name}")

		if(not isinstance(new_Area, area_type)):
			value_type_str = type(new_Area).__name__
			message = f"'__args__Option::{area_type_name}' must be of type '{area_type_name}' not '{value_type_str}'"
			raise Exception(message)

		setattr(self, f"_{area_type_name}", new_Area)


	# ———————————————————————————————————————— GETTERS & SETTERS::ATTRIBUTES  ———————————————————————————————————————— #

	def Area(self, new_Area: Optional[Area]=None) -> Optional[Area]:
		return self.get_or_set__args__(new_Area)


	def id(self):
		return self._id


	def is_activated(self, new_is_activated: Optional[bool]=None) -> Optional[bool]:
		if(new_is_activated is None):
			return self._is_activated

		if(not isinstance(new_is_activated, bool)):
			new_value_type: str = type(new_is_activated).__name__
			message = f"'AreaEvent[{self.__args__[0]}]::is_activated' must be of type 'bool' not '{new_value_type}'"
			raise Exception(message)

		self._is_activated = new_is_activated


	def is_deleted(self, new_is_deleted: Optional[bool]=None) -> Optional[bool]:
		if(new_is_deleted is None):
			return self._is_deleted

		if(not isinstance(new_is_deleted, bool)):
			new_value_type: str = type(new_is_deleted).__name__
			raise Exception(f"'AreaEvent[{self.__args__[0]}]::is_deleted' must be of type 'bool' not '{new_value_type}'")

		self._is_deleted = new_is_deleted


	def percentage(self, new_percentage: Optional[int]=None) -> Optional[int]:
		if(new_percentage is None):
			return self._percentage

		if(not isinstance(new_percentage, int)):
			new_value_type: str = type(new_percentage).__name__
			raise Exception(f"'AreaEvent[{self.__args__[0]}]::percentage' must be of type 'int' not '{new_value_type}'")

		self._percentage = new_percentage


	def Option(self, new_Option: Optional[Option]=None) -> Optional[Option]:
		if(new_Option is None):
			return self._Option

		if(not isinstance(new_Option, Option)):
			new_value_type: str = type(new_Option).__name__
			raise Exception(f"'AreaEvent[{self.__args__[0]}]::Option' must be of type 'Option' not '{new_value_type}'")

		self._Option = new_Option


	def time(self, new_time: Optional[datetime]=None) -> Optional[datetime]:
		if(new_time is None):
			return self._time

		if(not isinstance(new_time, datetime)):
			new_value_type: str = type(new_time).__name__
			raise Exception(f"'AreaEvent[{self.__args__[0]}]::time' must be of type 'datetime' not '{new_value_type}'")

		self._time = new_time


	# —————————————————————————————————————————————————— EXECUTION  —————————————————————————————————————————————————— #

	def __call__(self) -> None:
		"""
		SUMMARY: Activates an event by publishing it and cleaning up the resources
		"""
		self.publish()
		area_type = self.__args__[0]
		DB.DBFunctions.UPDATE_Events[area_type](self._id, is_activated=True)
		getattr(getattr(self, f"_{area_type.__name__}"), f"_{area_type.__name__}Events").remove(self)
		# `del self` is not required at this point, because the thread has successfully ended and should not rerun.


	def publish(self) -> None:
		from MQTT import MQTT_HOST

		area = getattr(self, f"_{self.__args__[0].__name__}")
		match(self.__args__[0]):
			case SmartCurtain.Home:
				topic = f"SmartCurtain/{area.id()}/move"
			case SmartCurtain.Room:
				topic = f"SmartCurtain/-/{area.id()}/move"
			case SmartCurtain.Curtain:
				topic = f"SmartCurtain/-/-/{area.id()}/move"
			case _:
				raise NotImplementedError(f"{self.__args__[0].__name__} is not an allowed template type")

		import sys
		print(payload := f"""[{topic}]""", file=sys.stderr, end=" ")
		print(payload := f"""{{"percentage": {self._percentage}}}""", file=sys.stderr)

		client = mqtt.client.Client()
		client.connect(MQTT_HOST, 1883, 60)
		client.publish(topic, payload)


	def start(self) -> None:
		# Set a thread for any event in the future
		if((now := datetime.now()) < self._time):
			self._publish_thread.start()

		# Run any event that was supposed to run in the last 5 seconds
		elif(now - timedelta(seconds=5) < self._time):  # IMPLICIT `self._time < now`
			self()

		# Ignore any other event
		else:
			area_type = self.__args__[0]

			DB.DBFunctions.UPDATE_Events[area_type](self._id, is_activated=True)

			getattr(getattr(self, f"_{area_type.__name__}"), f"_{area_type.__name__}Events").remove(self)
			# `del self` is not required at this point, because the thread was never started since it should only be
			#  started in this method.


	def sleep_time(self):
		if((now := datetime.now()) > self._time + timedelta(seconds=1)):
			Warn(f"Event {self._id} is scheduled at a time in the past")

		return (self._time - now).seconds if(now < self._time) else .25
