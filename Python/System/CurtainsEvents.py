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


	def Options_id(self) -> int:
		return self._Options_id;


	def desired_position(self, new_desired_position : Union[int, None]=None) -> Union[int, None]:
		if(isinstance(new_desired_position, type(None))): return self._desired_position;
		self._desired_position = new_desired_position;


	def is_activated(self, new_is_activated : Union[bool, None]=None) -> Union[bool, None]:
		if(isinstance(new_is_activated, type(None))): return self._is_activated;
		if(new_is_activated == self._is_activated): return True;

		from DB.DBFunctions import set_CurtainsEvent_activation;
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		success_flag = set_CurtainsEvent_activation(cnx, cursor, self._id)
		if(success_flag): self._is_activated = new_is_activated;
		__CLOSE__(cnx, cursor);

		return success_flag;


	def is_current(self, new_is_current : Union[bool, None]=None) -> Union[bool, None]:
		if(isinstance(new_is_current, type(None))): return self._is_current;
		self._is_current = new_is_current;


	def time(self, new_time : Union[int, None]=None) -> Union[int, None]:
		if(isinstance(new_time, type(None))): return self._time;
		self._time = new_time;


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
		return (self._time - now).seconds + 1 if (now < self._time) else 1;


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
