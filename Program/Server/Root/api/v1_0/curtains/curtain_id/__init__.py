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


import Server.Root.api.v1_0.curtains.curtain_id.events;
from System import System;


# `GET /api/v1_0/curtains/<int:curtain_id>`
# Show information for a curtain.
def GET(system: System, curtain_id: int):
	return str(system.Curtain(id=curtain_id));


# `PATCH /api/v1_0/curtains/<int:curtain_id>`
# Update information for curtain.
def PATCH(system: System, curtain_id: int):
	print(request.json);

	return str(system.Curtain(id=curtain_id));


# `DELETE /api/v1_0/curtains/<int:curtain_id>`
# Update information for curtain.
def DELETE(system: System, curtain_id: int):
	#TODO
	return str(system.Curtain(id=curtain_id));
