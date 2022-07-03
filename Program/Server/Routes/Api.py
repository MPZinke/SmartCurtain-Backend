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
from typing import Any;


import Utility.Logger as Logger;


def try_decorator(function: callable) -> callable:
	def wrapper(self, *args, **kwargs) -> Any:
		try:
			return function(self, *args, **kwargs);
		except KeyError as error:
			Logger.log_error(error);
			return {"error" : "{} missing from request".format(RE_search("'([^']*)'", error.message).group(1))};
		except Exception as error:
			Logger.log_error(error);
			return {"error" : "{}".format(str(error))};

	return wrapper;


# ————————————————————————————————————————————————————— CURTAINS ————————————————————————————————————————————————————— #
# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

# /api/curtains/<int:curtain_id>/is_activated/<int:is_activated>
@try_decorator
def api_curtains__id__is_activated__is_activated(self, curtain_id: int, is_activated: int):
	json = request.get_json();
	print(json);  #TESTING

	if(not (curtain := self._System.Curtain(id=curtain_id))):
		raise Exception("No curtain for ID found");
	# Scrub & validate data from JSON
	if(not isinstance((length := json["length"]), int)):
		raise Exception("\"length\" value is wrong type");
	if(not isinstance((percentage := json["percentage"]), int)):
		raise Exception("\"percentage\" value is wrong type");

	# Update curtain
	if(not curtain.is_activated(is_activated)):
		raise Exception("Unable to update Curtain activation");
	if(not curtain.length(length)):
		raise Exception("Unable to update length");
	if(not curtain.percentage(percentage)):
		raise Exception("Unable to update percentage");

	return {"success" : "Updated event"};


# ————————————————————————————————————————————————— CURTAINS::EVENTS ————————————————————————————————————————————————— #

# /api/curtains/<int:curtain_id>/events/new
@try_decorator
def api_curtains__id__events_new(self, curtain_id: int):
	json = request.get_json();
	print(json);  #TESTING

	if(not (curtain := self._System.Curtain(id=curtain_id))):
		raise Exception("No curtain for ID found");
	# Scrub & validate data from JSON
	if(not isinstance((percentage := json["percentage"]), int)):
		raise Exception("\"percentage\" value is wrong type");
	if(not isinstance((time := json["time"]), str)):
		raise Exception("\"time\" value is wrong type");

	# get/check curtain, convert time
	if(not (event_id := curtain.open(percentage, time=datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")))):
		raise Exception("Could not create event");
	return {"success" : "True", "event" : "{}".format(event_id)};


# /api/curtains/<int:curtain_id>/events/new/now
@try_decorator
def api_curtains__id__events_new_now(self, curtain_id: int):
	json = request.get_json();
	print(json);  #TESTING

	if(not (curtain := self._System.Curtain(id=curtain_id))):
		raise Exception("No curtain for ID found");
	# Scrub & validate data from JSON
	if(not isinstance((percentage := json["percentage"]), int)):
		raise Exception("\"desired percentage\" value is wrong type");

	if(not (event_id := curtain.open(percentage))):
		raise Exception("Could not create event");
	return {"success" : "True", "event" : "{}".format(event_id)};


# /api/curtains/<int:curtain_id>/events/new/now/close
@try_decorator
def api_curtains__id__events_new_now_close(self, curtain_id: int):
	json = request.get_json();

	if(not (curtain := self._System.Curtain(id=curtain_id))):
		raise Exception("No curtain for ID found");
	# Scrub & validate data from JSON
	if(not isinstance((percentage := json["percentage"]), int)):
		raise Exception("\"percentage\" value is wrong type");

	if(not (event_id := curtain.close())):
		raise Exception("Could not create event");
	return {"success" : "True", "event" : "{}".format(event_id)};


# /api/curtains/<int:curtain_id>/events/new/now/open
@try_decorator
def api_curtains__id__events_new_now_open(self, curtain_id):
	json = request.get_json();

	if(not (curtain := self._System.Curtain(id=curtain_id))):
		raise Exception("No curtain for ID found");
	if(not isinstance((percentage := json["percentage"]), int)):
		raise Exception("\"percentage\" value is wrong type");

	if(not (event_id := curtain.open())):
		raise Exception("Could not create event");
	return {"success" : "True", "event" : "{}".format(event_id)};


# ———————————————————————————————————————————— CURTAINS::GETTERS/SETTERS ———————————————————————————————————————————— #

# /api/curtains/<int:curtain_id>/is_activated
def api_curtains__id__is_activated(self, curtain_id: int):
	if(self._System.Curtain(id=curtain_id) is None):
		return {"error": True};

	if("percentage_percent__is_activated" in request.form):
		return str(self._System.Curtain(id=curtain_id));


# /api/curtains/<int:curtain_id>/deactivate
@try_decorator
def api_curtains__id__deactivate(self, curtain_id: int):
	json = request.get_json();
	print(json);  #TESTING

	if(not (curtain := self._System.Curtain(id=curtain_id))):
		raise Exception("No curtain for ID found");
	# Scrub & validate data from JSON
	if(not isinstance((length := json["length"]), int)):
		raise Exception("\"length\" value is wrong type");
	if(not isinstance((percentage := json["percentage"]), int)):
		raise Exception("\"percentage\" value is wrong type");

	if(not curtain.is_activated(False)):
		raise Exception("Unable to update Curtain activation");
	if(not curtain.percentage(percentage)):
		raise Exception("Unable to update percentage");

	return {"success" : "Updated Curtain"};



# —————————————————————————————————————————————————————— EVENTS —————————————————————————————————————————————————————— #

# LEGACY
# /api/update/deactivateevent
@try_decorator
def api_update_deactivateevent(self):
	json = request.get_json();

	if(not isinstance((curtain_id := json.get("curtain_id")), int)):
		raise Exception("\"curtain_id\" value is wrong type");

	return self.api_curtains__id__is_activated__is_activated(curtain_id, False);
