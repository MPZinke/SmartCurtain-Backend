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
from flask import request;


import Server.Root.api.v1_0.curtains.curtain_name.events;
from System import System;


# `GET /api/v1_0/curtains/<string:curtain_name>`
# Show information for a curtain.
def GET(system: System, curtain_name: str):
	return str(system.Curtain(name=curtain_name));


# `PATCH /api/v1_0/curtains/<int:curtain_name>`
# Show information for a curtain.
def PATCH(system: System, curtain_name: str):
	if((curtain := system.Curtain(name=curtain_name)) is None):
		raise Exception(f"No curtain for name '{curtain_name}' found")

	body = request.json;
	if("is_activated" in body):
		curtain.is_activated(body["is_activated"]);

	return str(curtain);
