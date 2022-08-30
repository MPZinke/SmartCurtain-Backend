#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.08.29                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import json;


from System import System;


def GET__index(system: System):
	return {
		"GET /api/v1.0/curtains/all": "Lists all curtains.",
		"POST /api/v1.0/curtains/new": "Creates a new curtain with the JSON body.",
		"GET /api/v1.0/curtains/<string:curtain_name|int:curtain_id>": "Show information for a curtain."
	};


def GET__all(system: System):
	return json.dumps([dict(curtain) for curtain in system.Curtains()], default=str);
