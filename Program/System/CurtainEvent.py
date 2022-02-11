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

from Other.Class.DBClass import DBClass;
from Other.Class.ZThreadSingle import ZThreadSingle;
from Other.DB.DBCredentials import *;
from Other.DB.DBFunctions import __CLOSE__, __CONNECT__;
from Other.DB.DBFunctions import SELECT_CurtainsEvents, INSERT_CurtainsEvents;
from Other.Global import *;
import Other.Logger as Logger;



class CurtainEvent(DBClass):

	# ———————————————————————————————————————————————— CON/DESTRUCTOR ———————————————————————————————————————————————— #

	def __init__(self, **event_info):
		DBClass.__init__(self, "UPDATE_CurtainsEvents", **event_info);

		from System.Curtain import Curtain as Curtain_Class;  # must be imported here to prevent circular importing
		keys = ["Curtain", "id", "desired_position", "is_activated", "is_current", "time"];
		types =	[Curtain_Class, int, [int, NONETYPE], [int, bool, NONETYPE], [int, bool, NONETYPE], datetime];
		CurtainEvent.validate_data(keys, types, event_info);

		self.__activation_thread = ZThreadSingle(f"Event Thread: {self._id}", self.activate, self.sleep_time);
		self.__activation_thread.start_thread(True);


	# Creates a new entry in the DB and returns the newly created CurtainEvent object
	@staticmethod
	def New(**info) -> object:
		# Check attributes are present
		from System.Curtain import Curtain as Curtain_Class;  # must be imported here to prevent circular importing
		keys = ["Curtain", "desired_position", "time"]
		types = [Curtain_Class, int, datetime]
		CurtainEvent.validate_data(keys, types, info);

		# Set possible missing attributes
		names, defaults = ["Options.id", "is_activated", "is_current"], [None, False, True];
		[info.update({name: info.get(name, defaults[x])}) for x, name in enumerate(names)];

		# Add to DB
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		event_params = [info["Curtain"].id(), info["Options.id"], info["desired_position"], info["time"]]
		info["id"] = INSERT_CurtainsEvents(cnx, cursor, *event_params);

		if(not info["id"]):
			__CLOSE__(cnx, cursor);
			raise Exception("Unable to add event to DB");
		__CLOSE__(cnx, cursor);

		# Return new instance of CurtainEvents
		return CurtainEvent(**info);


	def __del__(self):
		try: self.__activation_thread.kill();
		except: pass;


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
		Curtain = self._Curtain;

		post_json = self.json();
		print("Post data:", end="");  #TESTING
		print(post_json);  #TESTING
		try:
			if(not Curtain.is_smart() and Curtain.is_safe() and Curtain.current_position() == self._desired_position):
				raise Exception("Curtain will not move to a state it believes itself to already be in [is_safe=TRUE]");

			response = post(url=f"http://{Curtain.ip_address()}", json=post_json, timeout=buffer_time/10+1);
			if(response.status_code != 200): raise Exception(f"Status code for event: {self._id} is invalid");
			if("error" in response.json()): raise Exception(f"Received error message: {response.json()['error']}");
			print(response.json());  #TESTING

			if(not self.is_activated(True) or not self._is_activated): raise Exception("Failed to set event activated");
			if(not Curtain.is_activated(True)): raise Exception("Failed to set curtain activated");
			if(not Curtain.current_position(self._desired_position)): raise Exception("Failed to set curtain position");

		except Exception as error:
			Logger.log_error(error);

		self.delete();


	def json(self):
		Curtain = self._Curtain;
		System = Curtain.System();
		return	{
					"auto calibrate" : int(Curtain.CurtainOption("Auto Calibrate").is_on()),
					"auto correct" : int(Curtain.CurtainOption("Auto Correct").is_on()),

					"current position" : Curtain.current_position(), "direction" : int(Curtain.direction()),
					"is smart" : int(Curtain.is_smart()),
					"length" : Curtain.length(),

					"desired position" : self._desired_position if self._desired_position else 0,
					"event" : self._id
				};


	def sleep_time(self):
		now = datetime.now();
		time_plus_1_second = self._time + timedelta(seconds=1);
		if(time_plus_1_second < now): Warn("Event {} is scheduled at a time in the past".format(self._id));
		return (self._time - now).seconds if (now < self._time) else .25;


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self):
		attrs = ["_id", "_Curtains_id", "_Options_id", "_desired_position", "_is_activated", "_is_current", "_time"];
		return {attr : getattr(self, attr) for attr in attrs};


	def print(self, tab=0, next_tab=0):
		attrs = ["_id", "_Curtains_id", "_Options_id", "_desired_position", "_is_activated", "_is_current", "_time"];
		for attr in attrs: print('\t'*tab, attr, " : ", getattr(self, attr));
