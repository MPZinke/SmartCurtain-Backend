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


def GET__index(system: System):
	return {
		"GET /api/v1.0/curtains": "Lists options available related to Curtains.",
		"GET /api/v1.0/events": "Lists options available related to Events.",
		"GET /api/v1.0/options": "Lists options available related to Options."
	};
