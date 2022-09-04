#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.19                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime, timedelta;
from json import dumps;
import os;
import requests;
from typing import List, Union;


from Global import NONETYPE;
from System.CurtainOption import CurtainOption;
from System.DB import DBClass;
from System.DB import SELECT_CurtainsEvents_for_Curtains_id, SELECT_CurtainsEvents, SELECT_current_CurtainsEvents, \
  SELECT_CurtainsOptions;
from Utility import Logger;
from System.DB import AttributeType;


class Curtain(DBClass):
	ATTRIBUTE_TYPES =	[
							AttributeType("_id", int),
							AttributeType("_buffer_time", (int, bool, NONETYPE)),
							AttributeType("_percentage", (int, NONETYPE)),
							AttributeType("_direction", (int, bool, NONETYPE)),
							AttributeType("_is_activated", (int, bool, NONETYPE)),
							AttributeType("_is_current", (int, bool, NONETYPE)),
							AttributeType("_moves_discretely", (int, bool)),
							AttributeType("_port", (int, bool, NONETYPE)),
							AttributeType("_length", (int, bool, NONETYPE)),
							AttributeType("_name", str)
						];

	def __init__(self, **curtain_info):
		DBClass.__init__(self, "UPDATE_Curtains", **curtain_info);

		from System.CurtainEvent import CurtainEvent;

		# Get associated relations
		self._ip_address: str = self.lookup_curtain();
		assert(self._ip_address is not None), f"IP Address for '{self._name}' cannot be none"

		current_events = SELECT_current_CurtainsEvents(self._id);
		curtains_options = SELECT_CurtainsOptions(self._id);
		self._CurtainEvents = [CurtainEvent(**{**event, "Curtain": self}) for event in current_events];
		self._CurtainOptions = [CurtainOption(**option) for option in curtains_options];

		self.validate();


	def __iter__(self) -> dict:
		return DBClass.__iter__(self, "_CurtainEvents", "_CurtainOptions", "_ip_address");


	def __repr__(self) -> str:
		return str(self);


	def __str__(self) -> str:
		return dumps(dict(self), default=str);


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————
	# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————

	# Call event destructors, because they are not called simply from leaving scope, which leaves straggling threads.
	def delete_events(self):
		for curtain_event in self._CurtainEvents:
			curtain_event.delete();


	# ——————————————————————————————————— GETTERS/SETTERS::DB COLUMN SIMPLE QUERIES ———————————————————————————————————

	# Overwrite default DBCLass function for getting _id. This prevents it from being able to overwrite the value.
	def id(self) -> int:
		return self._id;


	def ip_address(self) -> str:
		return self._ip_address;


	# ———————————————————————————————————————————————— GETTERS: OBJECTS ————————————————————————————————————————————————

	def CurtainEvents(self) -> List["CurtainEvent"]:
		return self._CurtainEvents;


	# Gets the CurtainOption based on either name or id.
	# Takes a string or an int for the name of the CurtainOption.Option or the id of the CurtainOption.Option.id.
	def CurtainOption(self, **kwargs: dict) -> CurtainOption:
		return DBClass._exclusive_match(self._CurtainOptions, **kwargs);


	def CurtainOptions(self) -> List[CurtainOption]:
		return self._CurtainOptions;


	def System(self):
		return self._System;


	# ———————————————————————————————————————————————— GETTERS: SPECIAL ————————————————————————————————————————————————

	def CurtainEvent(self, **kwargs: dict) -> Union["CurtainEvent", None]:
		"""
		SUMMARY: Get CurtainsEvent if exists.
		PARAMS:  Takes the attribute name to match the event with.
		DETAILS: Checks whether the CurtainEvents exists in memory. If it doesn't, checks if it exists in the DB.
		RETURNS: Returns the Event if it is found, else None.
		"""
		from System.CurtainEvent import CurtainEvent;

		if((curtain_event := DBClass._exclusive_match(self._CurtainEvents, **kwargs)) is not None):
			return curtain_event;

		# Not found, check if in DB
		if((curtain_events := SELECT_CurtainsEvents_for_Curtains_id(self._id))):
			for event in curtain_events:
				# If found in DB, create an object and add to the list
				if(all(event.get(key) == value for key, value in kwargs)):
					curtain_event = CurtainEvent(**{**event, "Curtain": self});
					self._CurtainEvents.append(curtain_event);
					return curtain_event;

		return None;


	def CurtainEvents_for_range(self, *, latest: object=None, earliest: object=None) -> list:
		"""
		SUMMARY: Get all curtain events for a time range.
		PARAMS:  Takes the latest datetime time that an event can be, optionally the earliest datetime time an event can
		         be.
		DETAILS: Cycles through dictionary of events. If an event is within the range, event is added to list.
		RETURNS: A list of curtain events within that time range.
		"""
		if(not earliest and not latest):
			return [self._CurtainEvents[event_id] for event_id in self._CurtainEvents];

		events = [];
		for event in self._CurtainEvents:
			if((latest and latest < event.time()) or (earliest and event.time() < earliest)):
				continue;
			events.append(event);
		return events;


	def prior_CurtainEvents_for_current_day_of_week(self, earliest: object=None) -> list:
		earliest = earliest or datetime.today() - timedelta(days=28);

		#TODO: Get events for day of week.
		CurtainEvents_data = SELECT_CurtainsEvents();


	# ——————————————————————————————————————————————————— UTILITY ——————————————————————————————————————————————————— #

	def lookup_curtain(self: object) -> Union[str, None]:
		"""
		SUMMARY: Looks up the curtain from the NetworkLookup endpoint.
		PARAMS:  Takes the name of the curtain to lookup from NetworkLookup.
		DETAILS: Queries the NetworkLookup endpoint with the label for the curtain.
		RETURNS: The IP address string for the curtain.
		"""
		NetworkLookup_host = os.getenv("NETWORKLOOKUP_HOST");
		NetworkLookup_bearer_token = os.getenv("NETWORKLOOKUP_BEARERTOKEN");
		Curtain_network_name = os.getenv("SMARTCURTAIN_NETWORKNAME");

		url = f"http://{NetworkLookup_host}/api/v1.0/network/label/{Curtain_network_name}/device/label/{self._name}";
		response = requests.get(url, headers={"Authorization": f"Bearer {NetworkLookup_bearer_token}"});
		if(response.status_code == 200):
			try:
				return response.json()["address"];
			except Exception as error:
				print(error)

		return None;


	# ———————————————————————————————————————————————— EVENT CREATION ———————————————————————————————————————————————— #

	def _new_event(self, percentage: int=0, *, Options_id: int=None, time: object=None) -> int:
		from System.CurtainEvent import CurtainEvent;

		if(time is None):
			time = datetime.now();

		kwargs = {"Curtain": self, "Options.id": Options_id, "percentage": percentage, "time": time};
		if((curtain_event_dict := CurtainEvent.add_event_to_DB(**kwargs)) is None):
			raise Exception("Unable to add event to DB");

		curtain_event: CurtainEvent = CurtainEvent(**{**curtain_event_dict, "Curtain": self});
		self._CurtainEvents.append(curtain_event);

		return curtain_event.id();


	def close(self, *, Options_id: int=None, time: datetime=None):
		if(time is None):
			time = datetime.now();

		return self._new_event(0, Options_id=Options_id, time=time);


	def open(self, percentage: int=100, *, Options_id: int=None, time: object=None) -> int:
		if(time is None):
			time = datetime.now();

		return self._new_event(percentage, Options_id=Options_id, time=time);
