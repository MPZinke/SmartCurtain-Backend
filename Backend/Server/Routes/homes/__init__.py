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


from flask import request
import json
from werkzeug.exceptions import NotFound


from SmartCurtain import SmartCurtain


def GET(smart_curtain: SmartCurtain):
	"""
	`GET /homes`
	"""
	return json.dumps({home.id(): home.name() for home in smart_curtain.Homes()}, indent=4)


def GET_home_id(smart_curtain: SmartCurtain, home_id: int):
	"""
	`GET /homes/<int:home_id>`
	"""
	if((home := smart_curtain[home_id]) is None):
		raise NotFound(f"No home with id '{home_id}' was found")

	home_dict = dict(home)
	home_dict["Rooms"] = {room["id"]: room["name"] for room in home_dict["Rooms"]}
	return json.dumps(home_dict, indent=4, default=str)


def GET_home_id_rooms(smart_curtain: SmartCurtain, home_id: int):
	"""
	`GET /homes/<int:home_id>/rooms`
	"""
	if((home := smart_curtain[home_id]) is None):
		raise NotFound(f"No home with id '{home_id}' was found")

	home_dict = dict(home)
	return json.dumps({room["id"]: room["name"] for room in home_dict["Rooms"]}, indent=4)


def GET_home_id_curtains(smart_curtain: SmartCurtain, home_id: int):
	"""
	`GET /homes/<int:home_id>/curtains`
	"""
	if((home := smart_curtain[home_id]) is None):
		raise NotFound(f"No home with id '{home_id}' was found")

	return json.dumps({curtain.id(): curtain.name() for curtain in home["-"]}, indent=4)


def GET_home_id_events(smart_curtain: SmartCurtain, home_id: int):
	"""
	`GET /homes/<int:home_id>/events`
	"""
	if((home := smart_curtain[home_id]) is None):
		raise NotFound(f"No home with id '{home_id}' was found")

	return json.dumps([dict(event) for event in home.HomeEvents()], indent=4, default=str)


def POST(smart_curtain: SmartCurtain):
	pass
