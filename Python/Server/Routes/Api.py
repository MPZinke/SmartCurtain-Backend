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

		current_pos, curtain, event, length = [json[key] for key in ["current position", "curtain", "event", "length"]];
		if(not isinstance(curtain, int)): raise Exception("\\\"event\\\" value is not of correct type");
		print(json);  #TESTING

		curtain = self._System.Curtain(curtain);
		if(not curtain): raise Exception("No event for curtain found");
		if(not curtain.is_activated(False)): raise Exception("Unable to update Curtain activation");
		if(not curtain.current_position(current_pos)): raise Exception("Unable to update position");
		if(not curtain.length(length)): raise Exception("Unable to update length");

		return "{\"success\" : \"Updated event\"}";
	except Exception as error:
		log_error(error);
		return "{\"error\" : \"{}\"}".format(str(error));


# —————————————————————————————————————————————————————— BUILDERS ——————————————————————————————————————————————————————


