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


# `GET /homes`
def GET(smart_curtain: SmartCurtain) -> str:
	"""
	Lists all homes.
	"""
	return Response(json.dumps({home.id(): home.name() for home in smart_curtain.Homes()}), mimetype="application/json")


# `GET /homes/<int:home_id>`
def GET_home_id(smart_curtain: SmartCurtain, home_id: int) -> str:
	"""
	All information for a given home.
	"""
	if((home := smart_curtain[home_id]) is None):
		raise NotFound(f"No home with id '{home_id}' was found")

	home_dict = dict(home)
	home_dict["Rooms"] = {room["id"]: room["name"] for room in home_dict["Rooms"]}
	return Response(json.dumps(home_dict, default=str), mimetype="application/json")


# `GET /homes/<int:home_id>/rooms`
def GET_home_id_rooms(smart_curtain: SmartCurtain, home_id: int) -> str:
	"""
	Lists all rooms for a home given home.
	"""
	if((home := smart_curtain[home_id]) is None):
		raise NotFound(f"No home with id '{home_id}' was found")

	home_dict = dict(home)
	return Response(json.dumps({room["id"]: room["name"] for room in home_dict["Rooms"]}), mimetype="application/json")


# `GET /homes/<int:home_id>/curtains`
def GET_home_id_curtains(smart_curtain: SmartCurtain, home_id: int) -> str:
	"""
	Lists all for a home.
	"""
	if((home := smart_curtain[home_id]) is None):
		raise NotFound(f"No home with id '{home_id}' was found")

	return Response(json.dumps({curtain.id(): curtain.name() for curtain in home["-"]}), mimetype="application/json")


# `GET /homes/<int:home_id>/events`
def GET_home_id_events(smart_curtain: SmartCurtain, home_id: int) -> str:
	"""
	Lists all events for a home.
	"""
	if((home := smart_curtain[home_id]) is None):
		raise NotFound(f"No home with id '{home_id}' was found")

	return Response(json.dumps([dict(event) for event in home.HomeEvents()], default=str), mimetype="application/json")


def POST(smart_curtain: SmartCurtain) -> str:
	pass
