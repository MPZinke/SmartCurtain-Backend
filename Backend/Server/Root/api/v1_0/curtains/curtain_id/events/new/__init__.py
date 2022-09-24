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


from datetime import datetime;
from flask import request;
import json;


from SmartCurtain import SmartCurtain;


# `POST /api/v1.0/curtain/<int:curtain_id>/events/new`
# Creates a new curtain's event with the JSON body.
def POST(smart_curtain: SmartCurtain, curtain_id: int):
	if((curtain := smart_curtain.Curtain(id=curtain_id)) is None):
		raise Exception("Not found");  #TODO

	body: dict = request.json;
	if((percentage := body.get("percentage")) is None):
		raise Exception("Bad body");  #TODO
	kwargs = {"Options_id": body.get("Options.id")};
	kwargs["time"] = datetime.strptime("%Y-%m-%d %H:%M:%S", body["time"]) if("time" in body) else None;

	event_id = curtain._new_event(percentage, **kwargs);
	return json.dumps(dict(curtain.CurtainEvent(id=event_id)), default=str);
