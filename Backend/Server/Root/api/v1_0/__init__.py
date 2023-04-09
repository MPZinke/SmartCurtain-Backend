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


import Server.Root.api.v1_0.curtains;
import Server.Root.api.v1_0.events;
import Server.Root.api.v1_0.options;
from SmartCurtain import SmartCurtain;


def GET(smart_curtain: SmartCurtain):
	return {
		"GET /api/v1.0/curtains": "Lists options available related to Curtains.",
		"GET /api/v1.0/events": "Lists options available related to Events.",
		"GET /api/v1.0/options": "Lists options available related to Options."
	};
