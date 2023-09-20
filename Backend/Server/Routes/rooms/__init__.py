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


def GET(smart_curtain: SmartCurtain) -> str:
	"""
	`GET /rooms`
	"""
	return Response(json.dumps({room.id(): room.name() for room in smart_curtain["-"]}), mimetype="application/json")


def GET_room_id(smart_curtain: SmartCurtain, room_id: int) -> str:
	"""
	`GET /rooms/<int:room_id>`
	"""
	if((room := smart_curtain["-"][room_id]) is None):
		raise NotFound(f"No room with id '{room_id}' was found")

	room_dict = dict(room)
	room_dict["Curtains"] = {curtain["id"]: curtain["name"] for curtain in room_dict["Curtains"]}
	return Response(json.dumps(room_dict, default=str), mimetype="application/json")


def GET_room_id_curtains(smart_curtain: SmartCurtain, room_id: int) -> str:
	"""
	`GET /rooms/<int:room_id>/curtains`
	"""
	if((room := smart_curtain["-"][room_id]) is None):
		raise NotFound(f"No room with id '{room_id}' was found")

	return Response(json.dumps({curtain.id(): curtain.name() for curtain in room.Curtains()}, default=str),
		mimetype="application/json"
	)


def GET_room_id_events(smart_curtain: SmartCurtain, room_id: int) -> str:
	"""
	`GET /rooms/<int:room_id>/events`
	"""
	if((room := smart_curtain["-"][room_id]) is None):
		raise NotFound(f"No room with id '{room_id}' was found")

	return Response(json.dumps([dict(event) for event in room.RoomEvents()], default=str),
		mimetype="application/json"
	)


# `GET /rooms/<int:room_id>/structure`
def GET_room_id_structure(smart_curtain: SmartCurtain, room_id: int) -> str:
	"""
	Lists the structure a room is under.
	"""
	if((room := smart_curtain["-"][room_id]) is None):
		raise NotFound(f"No room with id '{room_id}' was found")

	home = room.Home()
	structure = {"room": {"id": room.id(), "name": room.name()}, "home": {"id": home.id(), "name": home.name()}}
	return Response(json.dumps(structure), mimetype="application/json")




def POST(smart_curtain: SmartCurtain) -> str:
	pass
