#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.09.03                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import Server.Root.api.v1_0.curtains.curtain_name.events.all;
import Server.Root.api.v1_0.curtains.curtain_name.events.new;
from SmartCurtain import SmartCurtain;


# `GET /api/v1.0/curtain/<string:curtain_name>/events`
# Lists options available related to curtains' events.
def GET(smart_curtain: SmartCurtain, curtain_name: str):
	return {
		f"GET /api/v1.0/curtains/{curtain_name}/events/all": "Lists all events for a curtain.",
		f"POST /api/v1.0/curtains/{curtain_name}/events/new": "Creates a new curtain's event with the JSON body.",
		f"GET /api/v1.0/curtains/{curtain_name}/event/<string:event_time>": "Show information for an event for a curtain."
	};
