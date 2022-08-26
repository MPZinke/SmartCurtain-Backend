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


# `GET /api`
# Lists the available API versions.
def GET__api(self):
	return {"GET /api/v1.0": "The current version of this API."}


# `GET /api/v1.0`
# Lists the available system parts.
def GET__api__v1_0(self):
	return {
		"GET /api/v1.0/curtains": "Lists options available related to Curtains.",
		"GET /api/v1.0/events": "Lists options available related to Events.",
		"GET /api/v1.0/options": "Lists options available related to Options."
	}


# `GET /api/v1_0/curtains`
# Lists options available related to Curtains.
def GET__api__v1_0__curtains(self):
	return {
		"GET /api/v1.0/curtains/all": "Lists all curtains.",
		"POST /api/v1.0/curtains/new": "Creates a new curtain with the JSON body.",
		"GET /api/v1.0/curtain/<string:curtain_name|int:curtain_id>": "Show information for a curtain."
	}


# `GET /api/v1_0/curtains/all`
# Lists all curtains.
def GET__api__v1_0__curtains__all(self):
	pass


# `POST /api/v1_0/curtains/new`
# Creates a new curtain with the JSON body.
def POST__api__v1_0__curtains__new(self):
	pass


# `GET /api/v1_0/curtain/<string:curtain_name>`
# Show information for a curtain.
def GET__api__v1_0__curtain__curtain_name(self, curtain_name: str):
	pass


# `GET /api/v1_0/curtain/<int:curtain_id>`
# Show information for a curtain.
def GET__api__v1_0__curtain__curtain_id(self, curtain_id: int):
	pass


# `PATCH /api/v1_0/curtain/<string:curtain_name>`
# Updates curtain's value(s) based on JSON body.
def PATCH__api__v1_0__curtain__curtain_name(self, **kwargs: dict):
	print(kwargs)
	pass


# `PATCH /api/v1_0/curtain/<int:curtain_id>`
# Updates curtain's value(s) based on JSON body.
def PATCH__api__v1_0__curtain__curtain_id(self, curtain_id: int):
	pass


# `GET /api/v1_0/curtain/<string:curtain_name|int:curtain_id>/events`
# Lists all events for a curtain.

# `GET /api/v1_0/curtain/<string:curtain_name>/events`
# Lists all events for a curtain.
def GET__api__v1_0__curtain__curtain_name__events(self, curtain_name: str):
	pass


# `GET /api/v1_0/curtain/<int:curtain_id>/events`
# Lists all events for a curtain.
def GET__api__v1_0__curtain__curtain_id__events(self, curtain_id: int):
	pass


# `GET /api/v1_0/curtain/<string:curtain_name|int:curtain_id>/event/<string:event_time|int:event_id>`
# Show information for an event for a curtain.

# `GET /api/v1_0/curtain/<string:curtain_name>/event/<string:event_time>`
# Show information for an event for a curtain.
def GET__api__v1_0__curtain__curtain_name__event__event_time(self, curtain_name: str, event_time: str):
	pass


# `GET /api/v1_0/curtain/<int:curtain_id>/event/<string:event_time>`
# Show information for an event for a curtain.
def GET__api__v1_0__curtain__curtain_id__event__event_time(self, curtain_id: int, event_time: str):
	pass


# `GET /api/v1_0/curtain/<string:curtain_name>/event/<int:event_id>`
# Show information for an event for a curtain.
def GET__api__v1_0__curtain__curtain_name__event__event_id(self, curtain_name: str, event_id: int):
	pass


# `GET /api/v1_0/curtain/<int:curtain_id>/event/<int:event_id>`
# Show information for an event for a curtain.
def GET__api__v1_0__curtain__curtain_id__event__event_id(self, curtain_id: int, event_id: int):
	pass


# `PATCH /api/v1_0/curtain/<string:curtain_name|int:curtain_id>/event/<string:event_time|int:event_id>`
# Updates curtain's events' value(s) based on JSON body.

# `PATCH /api/v1_0/curtain/<string:curtain_name>/event/<string:event_time>`
# Updates curtain's events' value(s) based on JSON body.
def PATCH__api__v1_0__curtain__curtain_name__event__event_time(self, curtain_name: str, event_time: str):
	pass


# `PATCH /api/v1_0/curtain/<int:curtain_id>/event/<string:event_time>`
# Updates curtain's events' value(s) based on JSON body.
def PATCH__api__v1_0__curtain__curtain_id__event__event_time(self, curtain_id: int, event_time: str):
	pass


# `PATCH /api/v1_0/curtain/<string:curtain_name>/event/<int:event_id>`
# Updates curtain's events' value(s) based on JSON body.
def PATCH__api__v1_0__curtain__curtain_name__event__event_id(self, curtain_name: str, event_id: int):
	pass


# `PATCH /api/v1_0/curtain/<int:curtain_id>/event/<int:event_id>`
# Updates curtain's events' value(s) based on JSON body.
def PATCH__api__v1_0__curtain__curtain_id__event__event_id(self, curtain_id: int, event_id: int):
	pass


# —————————————————————————————————————————————————————— EVENTS —————————————————————————————————————————————————————— #

# `GET /api/v1_0/events`—Lists options available related to Events.
def GET__api__v1_0__events(self):
	return {
		"GET /api/v1.0/events/all": "Lists all events.",
		"GET /api/v1.0/event/<int:event_id>": "Show information for an event.",
		"POST /api/v1.0/event/new": "Creates a new event with the JSON body."
	}


# `GET /api/v1_0/events/all`—Lists all events.
def GET__api__v1_0__events__all(self):
	pass


# `GET /api/v1_0/event/<int:event_id>`—Show information for an event.
def GET__api__v1_0__event__event_id(self, event_id: int):
	pass


# `POST /api/v1_0/event/new`—Creates a new event with the JSON body.
def POST__api__v1_0__event__new(self):
	pass


# ————————————————————————————————————————————————————— OPTIONS  ————————————————————————————————————————————————————— #

# `GET /api/v1_0/options`—Lists all events.
def GET__api__v1_0__options(self):
	return {
		"GET /api/v1.0/options/all": "Lists all options.",
		"GET /api/v1.0/option/<int:option_id>": "Show information for a curtain."
	}


# `GET /api/v1.0/options/all`—Lists all options.
def GET__api__v1_0__option__all(self):
	pass


# `GET /api/v1.0/option/<int:option_id>`—Show information for a curtain.
def GET__api__v1_0__option__option_id(self, option_id: int):
	pass



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
	if(not curtain.is_activated(bool(is_activated))):
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
