#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.25                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from flask import redirect, render_template, request, session;
from datetime import datetime;
from json import loads as JSON_loads;
from re import search as RE_search;

from Other.DB.DBCredentials import *;
from Other.DB.DBFunctions import __CONNECT__;
import Other.Logger as Logger;


# /api/create/future
def api_create_future(self):
	try:
		json = JSON_loads("["+request.get_json()+"]")[0];

		# get from JSON, check types
		curtain, desired_position, time = [json[key] for key in ["curtain", "desired position", "time"]];
		if(not isinstance(curtain, int)): raise Exception("\\\"event\\\" value is wrong type");
		if(not isinstance(desired_position, int)): raise Exception("\\\"desired position\\\" value is wrong type");

		# get/check curtain, convert time
		curtain = self._System.Curtain(curtain);
		if(not curtain): raise Exception("No curtain for ID found");
		time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S");
		# execute curtain
		event_id = curtain.open(desired_position=desired_position, time=time)
		if(not event_id): raise Exception("Could not create event");
		return "{\"success\" : \"True\", \"event\" : {}}".format(event_id);

	except Exception as error:
		Logger.log_error(error);
		if(not isinstance(error, KeyError)): return "{\"error\" : \"{}\"}".format(str(error));
		return "{\"error\" : \"{} missing from request\"}".format(RE_search("'([^']*)'", error.message).group(1));


# /api/create/now
def api_create_now(self):
	try:
		json = JSON_loads("["+request.get_json()+"]")[0];

		curtain, desired_position = [json[key] for key in ["curtain", "desired position"]];
		if(not isinstance(curtain, int)): raise Exception("\\\"curtain\\\" value is wrong type");
		if(not isinstance(desired_position, int)): raise Exception("\\\"desired position\\\" value is wrong type");

		curtain = self._System.Curtain(curtain);
		if(not curtain): raise Exception("No curtain for ID found");
		if(not curtain.open_immediately(desired_position)): raise Exception("Could not create event");
		return "{\"success\" : \"True\"}";

	except Exception as error:
		Logger.log_error(error);
		if(not isinstance(error, KeyError)): return "{\"error\" : \"{}\"}".format(str(error));
		return "{\"error\" : \"{} missing from request\"}".format(RE_search("'([^']*)'", error.message).group(1));


# ———————————————————————————————————————————————————— DEACTIVATE ———————————————————————————————————————————————————— #

# /api/update/deactivatecurtain
def api_update_deactivatecurtain(self):
	try:
		json = JSON_loads("["+request.get_json()+"]")[0];

		current_pos, curtain, event, length = [json[key] for key in ["current position", "curtain", "event", "length"]];
		if(not isinstance(current_pos, int)): raise Exception("\\\"current_pos\\\" value is wrong type");
		if(not isinstance(curtain, int)): raise Exception("\\\"curtain\\\" value is wrong type");
		if(not isinstance(event, int)): raise Exception("\\\"event\\\" value is wrong type");
		if(not isinstance(length, int)): raise Exception("\\\"length\\\" value is wrong type");
		print(json);  #TESTING

		curtain = self._System.Curtain(curtain);
		if(not curtain): raise Exception("No curtain for ID found");
		if(not curtain.is_activated(False)): raise Exception("Unable to update Curtain activation");
		if(not curtain.current_position(current_pos)): raise Exception("Unable to update position");
		if(not curtain.length(length)): raise Exception("Unable to update length");

		return "{\"success\" : \"Updated event\"}";

	except Exception as error:
		Logger.log_error(error);
		if(not isinstance(error, KeyError)): return "{\"error\" : \"{}\"}".format(str(error));
		return "{\"error\" : \"{} missing from request\"}".format(RE_search("'([^']*)'", error.message).group(1));


# /api/update/deactivateevent
def api_update_deactivateevent(self):
	try:
		json = request.get_json();
		print("Server::api_update_deactivateevent: ", end="");  #TESTING
		print(json);  #TESTING

		# Scrub & validate data from JSON
		keys = ["current position", "curtain", "event", "length"]
		current_position, curtain_id, event, length = [json.get(key) for key in keys];
		if(not isinstance(current_position, int)): raise Exception("\\\"current position\\\" value is wrong type");
		if(not isinstance(curtain_id, int)): raise Exception("\\\"curtain\\\" value is wrong type");
		if(not isinstance(event, int)): raise Exception("\\\"event\\\" value is wrong type");
		if(not isinstance(length, int)): raise Exception("\\\"length\\\" value is wrong type");

		# Update curtain
		curtain = self._System.Curtain(curtain_id);
		if(not curtain): raise Exception("No curtain for ID found");
		if(not curtain.is_activated(False)): raise Exception("Unable to update Curtain activation");
		if(not curtain.current_position(current_position)): raise Exception("Unable to update position");
		if(not curtain.length(length)): raise Exception("Unable to update length");

		return "{\"success\" : \"Updated event\"}";

	except Exception as error:
		Logger.log_error(error);
		if(not isinstance(error, KeyError)): return "{\"error\" : \"{}\"}".format(str(error));
		return "{\"error\" : \"{} missing from request\"}".format(RE_search("'([^']*)'", error.message).group(1));


# ———————————————————————————————————————————————————— INVALIDATE ———————————————————————————————————————————————————— #

def api_update_invalidateevent(self):
	try:
		json: dict = request.get_json();

		if("curtain" not in json): raise Exception("\\\"curtain\\\" value is missing from request");
		if("id" not in json["curtain"]): raise Exception("\\\"curtain::id\\\" value is missing from request");
		if("event" not in json): raise Exception("\\\"event\\\" value is missing from request");
		if("id" not in json["event"]): raise Exception("\\\"event::id\\\" value is missing from request");

		curtain_id = json["curtain"]["id"]
		event_id = json["event"]["id"];
		if(not isinstance(curtain_id, int)): raise Exception("\\\"event::id\\\" value is wrong type");
		if(not isinstance(event_id, int)): raise Exception("\\\"event::id\\\" value is wrong type");

		# if(not (curtain := self._System.Curtain(curtain_id))): raise Exception("No curtain for ID found");
		curtain = self._System.Curtain(curtain_id)
		if(not curtain): raise Exception("No curtain for ID found");
		# if(not (event := curtain.CurtainEvents().get(event_id))): raise Exception("No curtain event for ID found");
		event = curtain.CurtainEvents().get(event_id)
		if(not event): raise Exception("No curtain event for ID found");

		if(not event.delete()): raise Exception("Failed to delete event");

		return "{\"success\" : \"Deleted event\"}";

	except Exception as error:
		Logger.log_error(error);
		if(not isinstance(error, KeyError)): return "{\"error\" : \"{}\"}".format(str(error));
		return "{\"error\" : \"{} missing from request\"}".format(RE_search("'([^']*)'", error.message).group(1));


# —————————————————————————————————————————————————————— BUILDERS ——————————————————————————————————————————————————————


