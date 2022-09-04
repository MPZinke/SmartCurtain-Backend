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


from System import System;


def GET(system: System, event_id: int):
	for curtain in system.Curtains():
		if((event := curtain.CurtainEvent(id=event_id)) is not None):
			return dict(event)

	raise Exception(f"404: Event id {event_id} not found.");
