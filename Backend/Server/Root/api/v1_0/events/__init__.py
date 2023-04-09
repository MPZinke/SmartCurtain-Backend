#!/opt/homebrew/bin/python3
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


import Server.Root.api.v1_0.events.all;
import Server.Root.api.v1_0.events.event_id;
import Server.Root.api.v1_0.events.new;
from SmartCurtain import SmartCurtain;


def GET(smart_curtain: SmartCurtain):
	return {
		"GET /api/v1.0/events/all": "Lists all events.",
		"GET /api/v1.0/event/<int:event_id>": "Show information for an event.",
		"POST /api/v1.0/event/new": "Creates a new event with the JSON body."
	};
