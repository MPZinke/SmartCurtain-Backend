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


import Server.Root.api.v1_0.curtains.curtain_id.events.all;
import Server.Root.api.v1_0.curtains.curtain_id.events.new;
from System import System;


# `GET /api/v1.0/curtain/<int:curtain_id>/events`
# Lists options available related to curtains' events.
def GET(system: System, curtain_id: int):
	return {
		f"GET /api/v1.0/curtains/{curtain_id}/events/all": "Lists all events for a curtain.",
		f"POST /api/v1.0/curtains/{curtain_id}/events/new": "Creates a new curtain's event with the JSON body.",
		f"GET /api/v1.0/curtains/{curtain_id}/event/<string:event_time>": "Show information for an event for a curtain."
	};
