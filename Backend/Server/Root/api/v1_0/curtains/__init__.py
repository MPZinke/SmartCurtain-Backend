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


import Server.Root.api.v1_0.curtains.all;
import Server.Root.api.v1_0.curtains.curtain_id;
import Server.Root.api.v1_0.curtains.curtain_name;
from SmartCurtain import SmartCurtain;


def GET(smart_curtain: SmartCurtain):
	return {
		"GET /api/v1.0/curtains/all": "Lists all curtains.",
		"POST /api/v1.0/curtains/new": "Creates a new curtain with the JSON body.",
		"GET /api/v1.0/curtains/<string:curtain_name|int:curtain_id>": "Show information for a curtain."
	};
