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
from SmartCurtain import SmartCurtain;


# `GET /api/v1_0/curtains/<int:curtain_id>`
# Show information for a curtain.
def GET(smart_curtain: SmartCurtain, curtain_id: int):
	return str(smart_curtain.Curtain(id=curtain_id));


# `PATCH /api/v1_0/curtains/<int:curtain_id>`
# Show information for a curtain.
def PATCH(smart_curtain: SmartCurtain, curtain_id: int):
	if((curtain := smart_curtain.Curtain(id=curtain_id)) is None):
		raise Exception(f"No curtain for ID '{curtain_id}' found")

	body = request.json;
	if("is_activated" in body):
		curtain.is_activated(body["is_activated"]);

	return str(curtain);
