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
from DB.DBFunctions import __CONNECT__, mark_CurtainsEvents_as_complete;
from Other.Logger import log_error;


# /api/update/event
def api_update_event(self):
	try:
		json = request.get_json();
		for key in ["current position", "event", "length"]:
			if(key not in json): raise Exception("\\\"{}\\\" missing from request".format(key))
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		if(not isinstance(json["event"], int)): raise Exception("\\\"event\\\" value is not of correct type");
		if(mark_CurtainsEvents_as_complete(cnx, cursor, json["event"])): return "{\"success\" : \"Updated event\"}";
		raise Exception("Unable to update event");
	except Exception as error:
		log_error(error);
		return "{\"error\" : \"{}\"}".format(str(error));


# —————————————————————————————————————————————————————— BUILDERS ——————————————————————————————————————————————————————


