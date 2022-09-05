#!/usr/bin/env python3
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


from datetime import datetime, timedelta;
from json import dumps;
from requests import post;
from typing import List;
from warnings import warn as Warn;


from Global import *;
from System.Curtain import Curtain;
from System.DB import AttributeType, DBClass, ObjectAttributeType;
from System.DB import INSERT_CurtainsEvents;
from Utility.ZThread import ZThreadSingle;
from Utility import Logger;


class CurtainEvent(DBClass):
	ATTRIBUTE_TYPES =	[
							AttributeType("_Curtain", Curtain),
							AttributeType("_id", int),
							AttributeType("_percentage", (int, NONETYPE)),
							AttributeType("_is_activated", (int, bool, NONETYPE)),
							AttributeType("_is_current", (int, bool, NONETYPE)),
							AttributeType("_time", datetime)
						];

	# ———————————————————————————————————————————————— CON/DESTRUCTOR ———————————————————————————————————————————————— #

	def __init__(self, **event_info: dict):
		DBClass.__init__(self, "UPDATE_CurtainsEvents", **event_info);
		self.validate();

		self.__activation_thread = ZThreadSingle(f"Event Thread: {self._id}", self.activate, self.sleep_time);
		self.__activation_thread.start();


	# Creates a new entry in the DB and returns the newly created CurtainEvent object
	@staticmethod
	def add_event_to_DB(**info: dict) -> dict:
		# Check attributes are present
		# https://stackoverflow.com/a/19476841
		temp = type("Temp", (), {"Curtain": info["Curtain"], "percentage": info["percentage"], "time": info["time"]})();
		attribute_types: List[ObjectAttributeType] =[
														ObjectAttributeType(temp, AttributeType("Curtain", Curtain)),
														ObjectAttributeType(temp, AttributeType("percentage", int)),
														ObjectAttributeType(temp, AttributeType("time", datetime))
													];

		DBClass.validate(None, attribute_types);

		# Set possible missing attributes
		names_and_defaults = {"Options.id": None, "is_activated": False, "is_current": True};
		[info.update({name: info.get(name, default)}) for name, default in names_and_defaults.items()];

		# Add to DB
		event_params = [info["Curtain"].id(), info["Options.id"], info["percentage"], info["time"]];
		return INSERT_CurtainsEvents(*event_params);


	def __del__(self):
		try:
			self.__activation_thread.kill();
		except:
			return;


	def __iter__(self) -> dict:
		for x, attribute_type in enumerate(self.attribute_types):
			if(Curtain in attribute_type):
				del self.attribute_types[x];
				break;

		return DBClass.__iter__(self);


	def __repr__(self) -> str:
		return str(self);


	def __str__(self) -> str:
		return dumps(dict(self), default=str);


	def delete(self):
		# kill here since destructor doesn't kill very well
		try:
			self.__activation_thread.kill();
		# clear event from structure (later tater)
		finally:
			for x, event in enumerate(self._Curtain.CurtainEvents()):
				if(event.id() == self._id):
					del self._Curtain.CurtainEvents()[x];


	# ——————————————————————————————————— GETTERS/SETTERS::DB COLUMN SIMPLE QUERIES ———————————————————————————————————

	# Overwrite default DBCLass function for getting _id. This prevents it from being able to overwrite the value.
	def id(self) -> int:
		return self._id;


	# ———————————————————————————————————————————————————— ACTIVATE ————————————————————————————————————————————————————

	def activate(self):
		curtain = self._Curtain;

		post_dict = self.activation_dict();
		print("Post data:", end="");  #TESTING
		print(post_dict);  #TESTING
		try:
			response = post(url=f"http://{curtain.service()}", json=post_dict, timeout=curtain.buffer_time()/10+1);
			if(int(response.status_code / 100) != 2):
				raise Exception(f"Received {response.status_code} status code for event {self._id}");
			if("error" in response.json()):
				raise Exception(f"Received error message: {response.json()['error']}");
			print(response.json());  #TESTING

			if(not self.is_activated(True) or not self._is_activated):
				raise Exception("Failed to set event activated");

			curtain.is_activated(True);
			curtain.percentage(self._percentage);

		except Exception as error:
			Logger.log_error(error);

		self.delete();


	def activation_dict(self):
		return	{
					"query type": "move",
					"event":
					{
						"id" : self._id,
						"percentage": int(self._percentage) if self._percentage else 0,
					}
				};


	def sleep_time(self):
		now = datetime.now();
		time_plus_1_second = self._time + timedelta(seconds=1);
		if(time_plus_1_second < now):
			Warn(f"Event {self._id} is scheduled at a time in the past");

		return (self._time - now).seconds if (now < self._time) else .25;
