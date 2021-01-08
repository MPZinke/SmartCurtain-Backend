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
from DB.DBCredentials import *;
from DB.DBFunctions import __CONNECT__;
from Other.Logger import log_error;


# /api/update/event
def api_update_event(self):
	try:
		json = request.get_json();
		# validate
		if(any(key not in json for key in ["current position", "event", "length"])):
			raise Exception("\\\"{}\\\" missing from request".format(key));

		current_position, event, length = [json[key] for key in ["current position", "event", "length"]];
		if(not isinstance(event, int)): raise Exception("\\\"event\\\" value is not of correct type");

		curtain_for_event = self._System.Events_Curtain(event);
		if(not curtain_for_event): raise Exception("No event for curtain found");
		if(not curtain_for_event.CurtainsEvent_is_activated(True)): raise Exception("Unable to update event");
		if(not curtain_for_event.is_activated(False)): raise Exception("Unable to update Curtain activation");
		if(not curtain_for_event.current_position(current_position)): raise Exception("Unable to update position");
		if(not curtain_for_event.length(length)): raise Exception("Unable to update length");

		return "{\"success\" : \"Updated event\"}";
	except Exception as error:
		log_error(error);
		return "{\"error\" : \"{}\"}".format(str(error));


# —————————————————————————————————————————————————————— BUILDERS ——————————————————————————————————————————————————————


