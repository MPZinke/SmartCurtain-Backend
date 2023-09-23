#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2023.06.04                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from flask import request, Response
import json
from werkzeug.exceptions import NotFound


from SmartCurtain import SmartCurtain


# `GET /curtains`
def GET(smart_curtain: SmartCurtain) -> str:
	"""
	Lists information for all curtains.
	"""
	return Response(json.dumps({curtain.id(): curtain.name() for curtain in smart_curtain["-"]["-"]}),
		mimetype="application/json"
	)


# `GET /curtains/<int:curtain_id>`
def GET_curtain_id(smart_curtain: SmartCurtain, curtain_id: int) -> str:
	"""
	All information for a given curtain.
	"""
	if((curtain := smart_curtain["-"]["-"][curtain_id]) is None):
		raise NotFound(f"No curtain with id '{curtain_id}' was found")

	return Response(json.dumps(dict(curtain), default=str), mimetype="application/json")


# `GET /curtains/<int:curtain_id>/events`
def GET_curtain_id_events(smart_curtain: SmartCurtain, curtain_id: int) -> str:
	"""
	Lists events for a curtain.
	"""
	if((curtain := smart_curtain["-"]["-"][curtain_id]) is None):
		raise NotFound(f"No curtain with id '{curtain_id}' was found")

	return Response(json.dumps([dict(event) for event in curtain.CurtainEvents()], default=str),
		mimetype="application/json"
	)


# `GET /curtains/<int:curtain_id>/structure`
def GET_curtain_id_structure(smart_curtain: SmartCurtain, curtain_id: int) -> str:
	"""
	Lists the structure a room is under.
	"""
	if((curtain := smart_curtain["-"]["-"][curtain_id]) is None):
		raise NotFound(f"No curtain with id '{curtain_id}' was found")

	room = curtain.Room()
	home = room.Home()
	areas = {"curtain": curtain, "room": room, "home": home}
	structure = {name: {attr: getattr(area, attr)() for attr in ["id", "name"]} for name, area in areas.items()}
	return Response(json.dumps(structure), mimetype="application/json")


def POST(smart_curtain: SmartCurtain, curtain_id: int) -> str:
	print(request.data)
	return request.data
