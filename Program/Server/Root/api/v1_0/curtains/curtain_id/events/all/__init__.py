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


import json;


from System import System;


# `GET /api/v1.0/curtains/<int:curtain_id>/events/all`
# Lists all events for a curtain.
def GET(system: System, curtain_id: int):
	if((curtain := system.Curtain(id=curtain_id)) is None):
		raise Exception("Not found");  #TODO

	return json.dumps([dict(event) for event in curtain.CurtainEvents()], default=str);
