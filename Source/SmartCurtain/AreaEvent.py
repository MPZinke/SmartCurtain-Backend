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
from mpzinke import threading, typename, Generic
from paho import mqtt
from typing import Any, Optional, TypeVar
import warnings


import SmartCurtain
from SmartCurtain import Area
from SmartCurtain import DB
from SmartCurtain import Option


AreaEvent = TypeVar("AreaEvent")
Option = TypeVar("Option")


def wrong_type_string(instance: object, argument_name: str, required_type: type, supplied_value: Any) -> str:
	# "'{classname}::{argument_name}' must be of type '{required_type_name}' not '{supplied_type}'"
	message = "'{}::{}' must be of type '{}' not '{}'"
	return message.format(typename(instance), argument_name, required_type.__name__, typename(supplied_value))


class AreaEvent(Generic):
	def __init__(self, area: Optional[Area]=None, *, id: int, Option: Optional[object], is_activated: bool,
	  is_deleted: bool, percentage: int, time: datetime, **kwargs: dict
	):
		# STRUCTURE #
		self._Area: Optional[Area] = area

		getter = property(type(self).Area_getter)
		setter = getter.setter(type(self).Area_setter)
		setattr(type(self), f"Area", getter)  # EG `print(event.Area)`
		setattr(type(self), f"Area", setter)  # EG `event.Area = curtain`
		setattr(type(self), self.__args__[0].__name__, getter)  # EG `print(event.Curtain)`
		setattr(type(self), self.__args__[0].__name__, setter)  # EG `event.Curtain = curtain`
		setattr(type(self), f"_{self.__args__[0].__name__}", getter)  # EG `print(event._Curtain)`
		setattr(type(self), f"_{self.__args__[0].__name__}", setter)  # EG `event._Curtain = curtain`

		# DATABASE #
		self._id: int = id
		self.is_activated: bool = is_activated
		self.is_deleted: bool = is_deleted
		self.Option: Optional[object] = Option
		self.percentage: int = percentage
		self.time: datetime = time
		# THREAD #
		self._publish_thread = threading.DelayThread(f"Event Thread #{self._id}", action=self, time=self.sleep_time)


	@Generic
	def from_dictionary(__args__: set, curtain_event_data: dict) -> AreaEvent:
		option = Option(**curtain_event_data["Option"]) if(curtain_event_data["Option"] is not None) else None
		return AreaEvent[__args__[0]](**{**curtain_event_data, "Option": option})


	def __del__(self) -> None:
		# Kill the thread
		if(self._publish_thread.is_alive()):
			self._publish_thread.kill()

		# Remove from DB
		try:
			# Update DB.
			pass
		except:
			pass

		# Remove from memory
		try:
			self._Area.AreaEvents.remove(self)
		except Exception as error:
			warnings.warn(error)


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __eq__(self, right) -> bool:
		return self.id == right.id


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

	def Area_getter(self) -> Optional[Area]:
		return self._Area


	def Area_setter(self, new_Area) -> None:
		if(not isinstance(new_Area, self.__args__[0])):
			raise TypeError(wrong_type_string(self, "Area", self.__args__[0], new_Area))

		self._Area = new_Area


	@property
	def id(self):
		return self._id


	@property
	def is_activated(self) -> bool:
		return self._is_activated


	@is_activated.setter
	def is_activated(self, new_is_activated: bool):
		if(not isinstance(new_is_activated, bool)):
			raise TypeError(wrong_type_string(self, "is_activated", bool, new_is_activated))

		self._is_activated = new_is_activated


	@property
	def is_deleted(self) -> bool:
		return self._is_deleted


	@is_deleted.setter
	def is_deleted(self, new_is_deleted: bool) -> None:
		if(not isinstance(new_is_deleted, bool)):
			raise TypeError(wrong_type_string(self, "is_deleted", bool, new_is_deleted))

		self._is_deleted = new_is_deleted


	@property
	def percentage(self) -> int:
		return self._percentage


	@percentage.setter
	def percentage(self, new_percentage) -> int:
		if(not isinstance(new_percentage, int)):
			raise TypeError(wrong_type_string(self, "percentage", int, new_percentage))

		if(new_percentage < 0):
			warnings.warn(f"Percentage of '{new_percentage}' is being adjusted up to 0.")
			new_percentage = 0

		if(100 < new_percentage):
			warnings.warn(f"Percentage of '{new_percentage}' is being adjusted down to 100.")
			new_percentage = 0

		self._percentage = new_percentage


	@property
	def Option(self) -> Optional[Option]:
		return self._Option


	@Option.setter
	def Option(self, new_Option: Optional[Option]) -> None:
		if(new_Option is not None and not isinstance(new_Option, Option)):
			raise TypeError(wrong_type_string(self, "Option", Optional[Option], new_Option))

		self._Option = new_Option


	@property
	def time(self) -> datetime:
		return self._time


	@time.setter
	def time(self, new_time: datetime) -> None:
		if(not isinstance(new_time, datetime)):
			raise TypeError(wrong_type_string(self, "time", datetime, new_time))

		self._time = new_time


	# —————————————————————————————————————————————————— EXECUTION  —————————————————————————————————————————————————— #

	def __call__(self) -> None:
		"""
		SUMMARY: Activates an event by publishing it and cleaning up the resources
		"""
		self.publish()
		area_type = self.__args__[0]
		DB.DBFunctions.UPDATE_Events[area_type](self._id, is_activated=True)
		getattr(self._Area, f"_{area_type.__name__}Events").remove(self)
		# `del self` is not required at this point, because the thread has successfully ended and should not rerun.


	def publish(self) -> None:
		from MQTT import MQTT_HOST

		area = self._Area
		match(self.__args__[0]):
			case SmartCurtain.Home:
				topic = f"SmartCurtain/{area.id}/move"
			case SmartCurtain.Room:
				topic = f"SmartCurtain/-/{area.id}/move"
			case SmartCurtain.Curtain:
				topic = f"SmartCurtain/-/-/{area.id}/move"
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

			self._Area.AreaEvents.remove(self)
			# `del self` is not required at this point, because the thread was never started since it should only be
			#  started in this method.


	def sleep_time(self):
		if((now := datetime.now()) > self._time + timedelta(seconds=1)):
			warnings.warn(f"Event {self._id} is scheduled at a time in the past")

		return (self._time - now).seconds if(now < self._time) else .25
