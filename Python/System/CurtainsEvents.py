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
from typing import Union;
from warnings import warn as Warn;

from DB.DBCredentials import *;
from DB.DBFunctions import __CLOSE__, __CONNECT__;
from Class.ZThread import ZThread;


class CurtainsEvents:
	def __init__(self, event_info : dict, Curtain):
		self._Curtain = Curtain;

		self._id : int = event_info["id"];
		self._Curtains_id : int = event_info["Curtains.id"];
		self._Options_id : int = event_info["Options.id"];
		self._desired_position : int = event_info["desired_position"];
		self._is_activated : bool = bool(event_info["is_activated"]);
		self._is_current : bool = bool(event_info["is_current"]);
		self._time : object = event_info["time"];

		self.__activation_thread = ZThread("Event Thread: {}".format(self._id), self.activate, self.sleep_time);
		self.__activation_thread.start_thread(True);


	def __del__(self):
		try: self.__activation_thread.kill();
		except: pass;


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;


	def Curtains_id(self) -> int:
		return self._Curtains_id;


	# Helper function for managing what happens to DB data & attributes.
	# Take the name of the attribute that is affected & that setting value (if being set).
	# Sets a new value if a new value is passed.
	# Will return the original value if no new value is passed. Returns whether new value successfully set.
	def _get_or_set_attribute(self, attribute_name : str, new_value=None):
		if(isinstance(new_value, type(None))): return getattr(self, attribute_name);

		if(new_value == getattr(self, attribute_name)): return True;  # values match, take the easy way out
		# gotta update DB to match structure
		import DB.DBFunctions as DBFunctions;
		DB_function = getattr(DBFunctions, "set_CurtainsEvent"+attribute_name);
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		success_flag = DB_function(cnx, cursor, self._id, new_value);
		if(success_flag): setattr(self, attribute_name, new_value);
		return success_flag + bool(__CLOSE__(cnx, cursor));


	def Options_id(self) -> int:
		return self._Options_id;


	def desired_position(self, new_desired_position : Union[int, None]=None):
		return self._get_or_set_attribute("_desired_position", new_desired_position);


	def is_activated(self, new_is_activated : Union[bool, None]=None):
		return self._get_or_set_attribute("_is_activated", new_is_activated);


	def is_current(self, new_is_current : Union[bool, None]=None):
		return self._get_or_set_attribute("_is_current", new_is_current);


	def time(self, new_time : Union[int, None]=None):
		return self._get_or_set_attribute("_time", new_time);


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self):
		attrs = ["_id", "_Curtains_id", "_Options_id", "_desired_position", "_is_activated", "_is_current", "_time"];
		return {attr : getattr(self, attr) for attr in attrs};


	def print(self, tab=0, next_tab=0):
		attrs = ["_id", "_Curtains_id", "_Options_id", "_desired_position", "_is_activated", "_is_current", "_time"];
		for attr in attrs: print('\t'*tab, attr, " : ", getattr(self, attr));


	# ———————————————————————————————————————————————————— ACTIVATE ————————————————————————————————————————————————————

	def sleep_time(self):
		now = datetime.now();
		time_plus_1_second = self._time + timedelta(seconds=1);
		if(time_plus_1_second < now): Warn("Event {} is schedules at a time in the past".format(self._id));
		return (time_plus_1_second - now).seconds if (now < self._time) else 1;


	def activate(self):
		Curtain = self._Curtain;
		System = Curtain.System();
		post_json =	{
						"auto calibrate" : int(Curtain.CurtainsOption(System.Option_name("Auto Calibrate")).is_on()), 
						"auto correct" : int(Curtain.CurtainsOption(System.Option_name("Auto Correct")).is_on()),
						"current position" : Curtain.current_position(), "direction" : int(Curtain.direction()),
						"length" : Curtain.length(),
						"desired position" : self._desired_position if self._desired_position else 0, "event" : self._id
					};

		response = post(url=f"http://{Curtain.ip_address()}", json=post_json, timeout=3);
		if(response.status_code != 200): raise Exception(f"Status code for event: {self._id} is invalid");
		if("error" in response.json()): raise Exception(f"Received error message: {response.json()['error']}");

		print(response.json());  #TESTING
		if(not self.is_activated(True) or not self._is_activated): raise Exception("Could not set event as activated");
		if(not Curtain.is_activated(True)): raise Exception("Failed to set curtain as activated");

		self.__activation_thread.kill();  # stops current process
		# clear event from structure (later tater)
		CurtainEventsDict = Curtain.CurtainsEvents();
		if(self._id not in CurtainEventsDict): raise Exception("Event not found in Curtain Event dictionary");
		del CurtainEventsDict[self._id];