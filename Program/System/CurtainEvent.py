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
from requests import post;
from time import sleep;
from typing import List, Union;
from warnings import warn as Warn;


from Global import *;
from Utility.DBClass import AttributeType, AttributeValue, DBClass;
from Utility.DB import SELECT_CurtainsEvents, INSERT_CurtainsEvents;
from Utility.ZThread import ZThreadSingle;
import Utility.Logger as Logger;


class CurtainEvent(DBClass):

	# ———————————————————————————————————————————————— CON/DESTRUCTOR ———————————————————————————————————————————————— #

	def __init__(self, **event_info):
		DBClass.__init__(self, "UPDATE_CurtainsEvents", **event_info);

		from System.Curtain import Curtain as Curtain;  # must be imported here to prevent circular importing
		self.attribute_types: AttributeType =	[
													AttributeType("_Curtain", Curtain),
													AttributeType("_id", int),
													AttributeType("_percentage", [int, NONETYPE]),
													AttributeType("_is_activated", [int, bool, NONETYPE]),
													AttributeType("_is_current", [int, bool, NONETYPE]),
													AttributeType("_time", datetime)
												];
		self.validate();

		self.__activation_thread = ZThreadSingle(f"Event Thread: {self._id}", self.activate, self.sleep_time);
		self.__activation_thread.start_thread(True);


	# Creates a new entry in the DB and returns the newly created CurtainEvent object
	@staticmethod
	def New(**info) -> object:
		# Check attributes are present
		from System.Curtain import Curtain as Curtain;  # must be imported here to prevent circular importing
		validation_attributes: List[AttributeType] =	[
															AttributeType("Curtain", Curtain),
															AttributeType("percentage", int),
															AttributeType("time", datetime)
														];
		info_values: List[AttributeValue] =	[
												AttributeValue("Curtain", info["Curtain"]),
												AttributeValue("percentage", info["percentage"]),
												AttributeValue("time", info["time"])
											];

		CurtainEvent.validate_values(validation_attributes, info_values);

		# Set possible missing attributes
		names, defaults = ["Options.id", "is_activated", "is_current"], [None, False, True];
		[info.update({name: info.get(name, defaults[x])}) for x, name in enumerate(names)];

		# Add to DB
		event_params = [info["Curtain"].id(), info["Options.id"], info["percentage"], info["time"]]
		event_id: Union[int, None] = INSERT_CurtainsEvents(*event_params);

		if(event_id is None):
			raise Exception("Unable to add event to DB");

		# Return new instance of CurtainEvents
		return CurtainEvent(**info);


	def __del__(self):
		try:
			self.__activation_thread.kill();
		except:
			pass;


	def delete(self):
		# kill here since destructor doesn't kill very well
		try:
			self.__activation_thread.kill();
		# clear event from structure (later tater)
		finally:
			del self._Curtain.CurtainEvents()[self._id];


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
			if(not curtain.is_smart() and curtain.is_safe() and curtain.percentage() == self._percentage):
				raise Exception("Curtain will not move to a state it believes itself to already be in [is_safe=TRUE]");

			response = post(url=f"http://{curtain.ip_address()}", json=post_dict, timeout=curtain.buffer_time()/10+1);
			if(response.status_code != 200):
				raise Exception(f"Status code for event: {self._id} is invalid");
			if("error" in response.json()):
				raise Exception(f"Received error message: {response.json()['error']}");
			print(response.json());  #TESTING

			if(not self.is_activated(True) or not self._is_activated):
				raise Exception("Failed to set event activated");
			if(not curtain.is_activated(True)):
				raise Exception("Failed to set curtain activated");
			if(not curtain.percentage(self._percentage)):
				raise Exception("Failed to set curtain percentage");

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
			Warn("Event {} is scheduled at a time in the past".format(self._id));
		return (self._time - now).seconds if (now < self._time) else .25;


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self):
		attrs = ["_id", "_Curtains_id", "_Options_id", "_percentage", "_is_activated", "_is_current", "_time"];
		return {attr : getattr(self, attr) for attr in attrs};


	def print(self, tab=0, next_tab=0):
		attrs = ["_id", "_Curtains_id", "_Options_id", "_percentage", "_is_activated", "_is_current", "_time"];
		for attr in attrs:
			print('\t'*tab, attr, " : ", getattr(self, attr));
