#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2023.05.11                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   RESOURCES: - https://stackoverflow.com/a/71445989                                                                  #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from bson.objectid import ObjectId
from datetime import datetime
from flask import request, Response
import json
from mpzinke import typename, Generic, Server, Validator
from typing import Optional
from werkzeug.exceptions import BadRequest, NotFound


import SmartCurtain


# `GET /`
def GET(server: Server) -> str:
	"""
	Lists all all backend endpoints.
	"""
	# Uses `json.dumps` to keep order
	return Response(json.dumps(dict(server)), mimetype="application/json")


@Generic
def GET_area(__args__, smart_curtain: SmartCurtain.SmartCurtain) -> Response:
	match(__args__[0]):
		case SmartCurtain.Home:
			areas = smart_curtain.Homes
		case SmartCurtain.Room:
			areas = smart_curtain["-"]
		case SmartCurtain.Curtain:
			areas = smart_curtain["-"]["-"]
		case _:
			raise NotImplementedError(f"{__args__[0].__name__} is not an allowed template type")

	return Response(json.dumps({str(area.id): area.name for area in areas}), mimetype="application/json")


# `GET /[AREA]/<int:area_id>`
@Generic
def GET_area_id(__args__, smart_curtain: SmartCurtain.SmartCurtain, area_id: str) -> Response:
	"""
	All information for a given area.
	"""
	area_id = ObjectId(area_id)
	match(__args__[0]):
		case SmartCurtain.Home:
			area = smart_curtain[area_id]
		case SmartCurtain.Room:
			area = smart_curtain["-"][area_id]
		case SmartCurtain.Curtain:
			area = smart_curtain["-"]["-"][area_id]
		case _:
			raise NotImplementedError(f"{__args__[0].__name__} is not an allowed template type")

	if(area is None):
		raise NotFound(f"No {__args__[0].__name__} with id '{area_id}' was found")

	return Response(json.dumps(dict(area), default=str), mimetype="application/json")


# `GET /[AREA]/<int:area_id>/events`
@Generic
def GET_area_id_events(__args__, smart_curtain: SmartCurtain.SmartCurtain, area_id: str) -> str:
	"""
	Lists events for a {__args___names[0]}.
	"""
	area_id = ObjectId(area_id)
	match(__args__[0]):
		case SmartCurtain.Home:
			area = smart_curtain[area_id]
		case SmartCurtain.Room:
			area = smart_curtain["-"][area_id]
		case SmartCurtain.Curtain:
			area = smart_curtain["-"]["-"][area_id]
		case _:
			raise NotImplementedError(f"{__args__[0].__name__} is not an allowed template type")

	if(area is None):
		raise NotFound(f"No {__args__[0].__name__} with id '{area_id}' was found")

	return Response(json.dumps([dict(event) for event in area.AreaEvents], default=str), mimetype="application/json")


# `GET /[AREA]/<int:area_id>/structure`
@Generic
def GET_area_id_structure(__args__, smart_curtain: SmartCurtain.SmartCurtain, area_id: str) -> str:
	"""
	Lists the structure a room is under.
	"""
	area_id = ObjectId(area_id)
	match(__args__[0]):
		case SmartCurtain.Home:
			area = smart_curtain[area_id]
			areas = {"home": area}
		case SmartCurtain.Room:
			area = smart_curtain["-"][area_id]
			areas = {"room": area, "home": area.Home}
		case SmartCurtain.Curtain:
			area = smart_curtain["-"]["-"][area_id]
			room = area.Room
			areas = {"curtain": area, "room": room, "home": room.Home}
		case _:
			raise NotImplementedError(f"{__args__[0].__name__} is not an allowed template type")

	if(area is None):
		raise NotFound(f"No {__args__[0].__name__} with id '{area_id}' was found")

	structure = {name: {attr: getattr(area, attr) for attr in ["id", "name"]} for name, area in areas.items()}
	return Response(json.dumps(structure, default=str), mimetype="application/json")


@Generic
def POST_area_id_events(__args__, smart_curtain: SmartCurtain.SmartCurtain, area_id: str) -> str:
	area_id = ObjectId(area_id)
	match(__args__[0]):
		case SmartCurtain.Home:
			area = smart_curtain[area_id]
		case SmartCurtain.Room:
			area = smart_curtain["-"][area_id]
		case SmartCurtain.Curtain:
			area = smart_curtain["-"]["-"][area_id]
		case _:
			raise NotImplementedError(f"{__args__[0].__name__} is not an allowed template type")

	if(area is None):
		raise NotFound(f"No {__args__[0].__name__} with id '{area_id}' was found")

	event_data = request.json
	Validator.check_for_missing_arguments(event_data, {"percentage": int, "option": Optional[int], "time": str})
	Validator.check_argument_types(event_data, {"percentage": int, "option": Optional[int], "time": str})
	percentage, option, time = event_data["percentage"], event_data["option"], event_data["time"]

	try:
		time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
	except Exception as error:
		raise BadRequest(f"'{time}' if not of proper format '%Y-%m-%d %H:%M:%S'") from error

	event = area.new_AreaEvent(is_activated=False, percentage=percentage, option_id=option, time=time)
	return Response(json.dumps(dict(event), default=str), mimetype="application/json")


@Generic
def GET_area_id_event_id(__args__, smart_curtain: SmartCurtain.SmartCurtain, area_id: str, event_id: int):
	area_id = ObjectId(area_id)
	match(__args__[0]):
		case SmartCurtain.Home:
			area = smart_curtain[area_id]
		case SmartCurtain.Room:
			area = smart_curtain["-"][area_id]
		case SmartCurtain.Curtain:
			area = smart_curtain["-"]["-"][area_id]
		case _:
			raise NotImplementedError(f"{__args__[0].__name__} is not an allowed template type")

	if((event := next((event for event in area.AreaEvents if(event.id == event_id)), None)) is None):
		raise NotFound(f"Event with id '{event_id}' not found for {__args__[0].__name__} '{area_id}'")

	return Response(json.dumps(dict(event), default=str), mimetype="application/json")


@Generic
def PATCH_area_id_event_id(__args__, smart_curtain: SmartCurtain.SmartCurtain, area_id: str, event_id: int):
	area_id = ObjectId(area_id)
	match(__args__[0]):
		case SmartCurtain.Home:
			area = smart_curtain[area_id]
		case SmartCurtain.Room:
			area = smart_curtain["-"][area_id]
		case SmartCurtain.Curtain:
			area = smart_curtain["-"]["-"][area_id]
		case _:
			raise NotImplementedError(f"{__args__[0].__name__} is not an allowed template type")

	if((event := next((event for event in area.AreaEvents if(event.id == event_id)), None)) is None):
		raise NotFound(f"Event with id '{event_id}' not found for {__args__[0].__name__} '{area_id}'")

	#TODO: Update event

	return Response(json.dumps(dict(event), default=str), mimetype="application/json")


@Generic
def DELETE_area_id_event_id(__args__, smart_curtain: SmartCurtain.SmartCurtain, area_id: str, event_id: int):
	area_id = ObjectId(area_id)
	match(__args__[0]):
		case SmartCurtain.Home:
			area = smart_curtain[area_id]
		case SmartCurtain.Room:
			area = smart_curtain["-"][area_id]
		case SmartCurtain.Curtain:
			area = smart_curtain["-"]["-"][area_id]
		case _:
			raise NotImplementedError(f"{__args__[0].__name__} is not an allowed template type")

	del area[event_id]
	return "", 204


def GET_options(smart_curtain: SmartCurtain.SmartCurtain):
	options = smart_curtain.Options
	return Response(json.dumps(list(map(dict, options)), default=str), mimetype="application/json")
