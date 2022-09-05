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


from System import System;


import Server.Root.api.v1_0.options.all;
import Server.Root.api.v1_0.options.option_id;
import Server.Root.api.v1_0.options.option_name;


def GET(system: System):
	return {
		"GET /api/v1.0/options/all": "Lists all options.",
		"GET /api/v1.0/option/<int:option_id>": "Show information for a curtain.",
		"GET /api/v1.0/option/<int:option_name>": "Show information for a curtain."
	};
