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
	return json.dumps({home.id(): home.name() for home in smart_curtain.Homes()}, indent=4)


def GET_homes_id(smart_curtain: SmartCurtain, homes_id: int):
	if((home := smart_curtain[homes_id]) is not None):
		home_dict = dict(home)
		home_dict["Rooms"] = {room["id"]: room["name"] for room in home_dict["Rooms"]}
		return json.dumps(home_dict, indent=4)

	raise NotFound(f"No home with id '{homes_id}' was found")


def POST(smart_curtain: SmartCurtain):
	pass
