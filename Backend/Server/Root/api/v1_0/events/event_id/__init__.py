#!/opt/homebrew/bin/python3
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


from SmartCurtain import SmartCurtain;


# `GET /api/v1_0/events/<int:event_id>`
# Lists options available related to Events.
def GET(smart_curtain: SmartCurtain, event_id: int):
	for curtain in smart_curtain.Curtains():
		if((event := curtain.CurtainEvent(id=event_id)) is not None):
			return json.dumps(dict(event), default=str);

	raise Exception(f"404: Event id {event_id} not found.");


# `PATCH /api/v1_0/events/<int:event_id>`
# Update information for event.
def PATCH(smart_curtain: SmartCurtain, event_id: int):
	for curtain in smart_curtain.Curtains():
		if((event := curtain.CurtainEvent(id=event_id)) is not None):
			#TODO
			return json.dumps(dict(event), default=str);

	raise Exception(f"404: Event id {event_id} not found.");


# `DELETE /api/v1_0/events/<int:event_id>`
# Update information for event.
def DELETE(smart_curtain: SmartCurtain, event_id: int):
	for curtain in smart_curtain.Curtains():
		if((event := curtain.CurtainEvent(id=event_id)) is not None):
			#TODO
			return json.dumps(dict(event), default=str);

	raise Exception(f"404: Event id {event_id} not found.");
