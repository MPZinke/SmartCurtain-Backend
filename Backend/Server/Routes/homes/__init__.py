#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2023.05.12                                                                                                      #
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
	`GET /homes`
	"""
	return Response(json.dumps({home.id(): home.name() for home in smart_curtain.Homes()}), mimetype="application/json")


def GET_home_id(smart_curtain: SmartCurtain, home_id: int) -> str:
	"""
	`GET /homes/<int:home_id>`
	"""
	if((home := smart_curtain[home_id]) is None):
		raise NotFound(f"No home with id '{home_id}' was found")

	home_dict = dict(home)
	home_dict["Rooms"] = {room["id"]: room["name"] for room in home_dict["Rooms"]}
	return Response(json.dumps(home_dict, default=str), mimetype="application/json")


def GET_home_id_rooms(smart_curtain: SmartCurtain, home_id: int) -> str:
	"""
	`GET /homes/<int:home_id>/rooms`
	"""
	if((home := smart_curtain[home_id]) is None):
		raise NotFound(f"No home with id '{home_id}' was found")

	home_dict = dict(home)
	return Response(json.dumps({room["id"]: room["name"] for room in home_dict["Rooms"]}), mimetype="application/json")


def GET_home_id_curtains(smart_curtain: SmartCurtain, home_id: int) -> str:
	"""
	`GET /homes/<int:home_id>/curtains`
	"""
	if((home := smart_curtain[home_id]) is None):
		raise NotFound(f"No home with id '{home_id}' was found")

	return Response(json.dumps({curtain.id(): curtain.name() for curtain in home["-"]}), mimetype="application/json")


def GET_home_id_events(smart_curtain: SmartCurtain, home_id: int) -> str:
	"""
	`GET /homes/<int:home_id>/events`
	"""
	if((home := smart_curtain[home_id]) is None):
		raise NotFound(f"No home with id '{home_id}' was found")

	return Response(json.dumps([dict(event) for event in home.HomeEvents()], default=str), mimetype="application/json")


def GET_home_id_structure(smart_curtain: SmartCurtain, home_id: int) -> str:
	"""
	`GET /homes/<int:home_id>/structure`
	"""
	if((home := smart_curtain[home_id]) is None):
		raise NotFound(f"No home with id '{home_id}' was found")

	home_structure: dict = {"id": home.id(), "name": home.name(), "rooms": []}
	for room in home.Rooms():
		room_dict = {"id": room.id(), "name": room.name(), "curtains": []}

		for curtain in room.Curtains():
			room_dict["curtains"].append({"id": curtain.id(), "name": curtain.name()})

		home_structure["rooms"].append(room_dict)

	return Response(json.dumps(home_structure, default=str), mimetype="application/json")


def POST(smart_curtain: SmartCurtain) -> str:
	pass
