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


def try_decorator(function):
	def wrapper(self, *args):
		try:
			return function(self, *args);
		except KeyError as error:
			Logger.log_error(error);
			return "{\"error\" : \"{} missing from request\"}".format(RE_search("'([^']*)'", error.message).group(1));
		except Exception as error:
			Logger.log_error(error);
			return "{\"error\" : \"{}\"}".format(str(error));

	return wrapper;


# ————————————————————————————————————————————————————— CURTAINS ————————————————————————————————————————————————————— #

# /api/curtains/<int:curtain_id>/is_activated
def api_curtains__id__is_activated(self, curtain_id: int):
	if(curtain_id not in self._System.Curtains()): return {"error"};

	if("current_position_percent__is_activated" in request.form):
		return str(self._System.Curtain(curtain_id));


# /api/curtains/<int:curtain_id>/is_activated/<int:is_activated>
@try_decorator
def api_curtains__id__is_activated__is_activated(self, curtain_id: int, is_activated: int):
	json = request.get_json();
	print("Server::api_update_deactivateevent: ", end="");  #TESTING
	print(json);  #TESTING

	# Scrub & validate data from JSON
	keys = ["current position", "event", "length"]
	current_position, event_id, length = [json.get(key) for key in keys];
	if(not isinstance(current_position, int)): raise Exception("\\\"current position\\\" value is wrong type");
	if(not isinstance(curtain_id, int)): raise Exception("\\\"curtain\\\" value is wrong type");
	if(not isinstance(length, int)): raise Exception("\\\"length\\\" value is wrong type");

	# Update curtain
	curtain = self._System.Curtain(curtain_id);
	if(not curtain): raise Exception("No curtain for ID found");
	if(not curtain.is_activated(is_activated)): raise Exception("Unable to update Curtain activation");
	if(not curtain.current_position(current_position)): raise Exception("Unable to update position");
	if(not curtain.length(length)): raise Exception("Unable to update length");

	return "{\"success\" : \"Updated event\"}";


# /api/curtains/<int:curtain_id>/event/new/future
@try_decorator
def api_curtains__id__event_new_future(self):
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



# /api/curtains/<int:curtain_id>/event/new/now
@try_decorator
def api_curtains__id__event_new_now(self):
	json = JSON_loads("["+request.get_json()+"]")[0];

	curtain, desired_position = [json[key] for key in ["curtain", "desired position"]];
	if(not isinstance(curtain, int)): raise Exception("\\\"curtain\\\" value is wrong type");
	if(not isinstance(desired_position, int)): raise Exception("\\\"desired position\\\" value is wrong type");

	curtain = self._System.Curtain(curtain);
	if(not curtain): raise Exception("No curtain for ID found");
	if(not curtain.open_immediately(desired_position)): raise Exception("Could not create event");
	return "{\"success\" : \"True\"}";


# /api/curtains/<int:curtain_id>/deactivate
@try_decorator
def api_curtains__id__deactivate(self, curtain_id: int):
	json = JSON_loads("["+request.get_json()+"]")[0];

	current_pos, event, length = [json[key] for key in ["current position", "event", "length"]];
	if(not isinstance(current_pos, int)): raise Exception("\\\"current_pos\\\" value is wrong type");
	if(not isinstance(event, int)): raise Exception("\\\"event\\\" value is wrong type");
	if(not isinstance(length, int)): raise Exception("\\\"length\\\" value is wrong type");
	print(json);  #TESTING

	curtain = self._System.Curtain(curtain_id);
	if(not curtain): raise Exception("No curtain for ID found");
	if(not curtain.is_activated(False)): raise Exception("Unable to update Curtain activation");
	if(not curtain.current_position(current_pos)): raise Exception("Unable to update position");
	if(not curtain.length(length)): raise Exception("Unable to update length");

	return "{\"success\" : \"Updated Curtain\"}";



# —————————————————————————————————————————————————————— EVENTS —————————————————————————————————————————————————————— #

# LEGACY
# /api/update/deactivateevent
@try_decorator
def api_update_deactivateevent(self):
	json = request.get_json();

	curtain_id = json.get("curtain");
	if(not isinstance(curtain_id, int)): raise Exception("\\\"curtain\\\" value is wrong type");

	return self.api_curtains__id__is_activated__is_activated(curtain_id, False);
