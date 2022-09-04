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


# `PATCH /api/v1_0/curtains/<string:curtain_name>`
# Update information for curtain.
def PATCH(system: System, curtain_name: str):
	print(request.json);

	return str(system.Curtain(name=curtain_name));


# `DELETE /api/v1_0/curtains/<string:curtain_name>`
# Update information for curtain.
def DELETE(system: System, curtain_name: str):
	#TODO
	return str(system.Curtain(name=curtain_name));
