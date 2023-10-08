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
from typing import Optional
import warnings


import SmartCurtain
from SmartCurtain import DB
from Utility import wrong_type_string


class AreaEvent(Generic):
	def __init_subclass__(cls):
		getter = property(cls.Area_getter)
		setter = getter.setter(cls.Area_setter)
		setattr(cls, "Area", getter)  # EG `print(event.Area)`
		setattr(cls, "Area", setter)  # EG `event.Area = curtain`
		setattr(cls, cls.__args__[0].__name__, getter)  # EG `print(event.Curtain)`
		setattr(cls, cls.__args__[0].__name__, setter)  # EG `event.Curtain = curtain`


	def __init__(self, Area: Optional[SmartCurtain.Area]=None, *, id: int, Option: Optional[SmartCurtain.Option],
		is_activated: bool, is_deleted: bool, percentage: int, time: datetime
	):
		# STRUCTURE #
		self.Area: Optional[SmartCurtain.Area] = Area
		# DATABASE #
		assert(isinstance(id, int)), wrong_type_string(self, "id", int, id)
		self._id: int = id
		self.is_activated: bool = is_activated
		self.is_deleted: bool = is_deleted
		self.Option: Optional[SmartCurtain.Option] = Option
		self.percentage: int = percentage
		self.time: datetime = time
		# THREAD #
		self._publish_thread = threading.DelayThread(f"Event Thread #{self._id}", action=self, time=self.sleep_time)


	@Generic
	def from_dictionary(__args__: set, curtain_event_data: dict) -> SmartCurtain.AreaEvent:
		option = SmartCurtain.Option(**curtain_event_data["Option"]) if(curtain_event_data["Option"]) else None
		return SmartCurtain.AreaEvent[__args__[0]](**{**curtain_event_data, "Option": option})


	def __del__(self) -> None:
		print(f"Killing event with id '{self.id}'")
		# Kill the thread
		if(self._publish_thread.is_alive()):
			self._publish_thread.kill()

		# Remove from DB
		try:
			# Update DB.
			pass
		except:
			pass


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __eq__(self, right: SmartCurtain.AreaEvent) -> bool:
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

	def Area_getter(self) -> Optional[SmartCurtain.Area]:
		return self._Area


	def Area_setter(self, new_Area: Optional[SmartCurtain.Area]) -> None:
		if(not isinstance(new_Area, Optional[self.__args__[0]])):
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
	def percentage(self, new_percentage: int) -> int:
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
	def Option(self) -> Optional[SmartCurtain.Option]:
		return self._Option


	@Option.setter
	def Option(self, new_Option: Optional[SmartCurtain.Option]) -> None:
		if(new_Option is not None and not isinstance(new_Option, SmartCurtain.Option)):
			raise TypeError(wrong_type_string(self, "Option", Optional[SmartCurtain.Option], new_Option))

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
		DB.DBFunctions.UPDATE_Events[self.__args__[0]](self._id, is_activated=True)
		self._Area._AreaEvents.remove(self)  # `._AreaEvents` so that the event is removed from the saved list
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
			DB.DBFunctions.UPDATE_Events[self.__args__[0]](self._id, is_activated=True)

			self._Area.AreaEvents.remove(self)
			# `del self` is not required at this point, because the thread was never started since it should only be
			#  started in this method.


	def sleep_time(self):
		if((now := datetime.now()) > self._time + timedelta(seconds=1)):
			warnings.warn(f"Event {self._id} is scheduled at a time in the past")

		return (self._time - now).seconds if(now < self._time) else .25
