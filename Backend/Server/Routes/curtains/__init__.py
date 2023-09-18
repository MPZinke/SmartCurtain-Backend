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
	`GET /curtains`
	"""
	return Response(json.dumps({curtain.id(): curtain.name() for curtain in smart_curtain["-"]["-"]}),
		mimetype="application/json"
	)


def GET_curtain_id(smart_curtain: SmartCurtain, curtain_id: int) -> str:
	"""
	`GET /curtains/<int:curtain_id>`
	"""
	if((curtain := smart_curtain["-"]["-"][curtain_id]) is None):
		raise NotFound(f"No curtain with id '{curtain_id}' was found")

	return Response(json.dumps(dict(curtain), default=str), mimetype="application/json")


def GET_curtain_id_events(smart_curtain: SmartCurtain, curtain_id: int) -> str:
	"""
	`GET /curtains/<int:curtain_id>/events`
	"""
	if((curtain := smart_curtain["-"]["-"][curtain_id]) is None):
		raise NotFound(f"No curtain with id '{curtain_id}' was found")

	return Response(json.dumps([dict(event) for event in curtain.CurtainEvents()], default=str),
		mimetype="application/json"
	)


def POST(smart_curtain: SmartCurtain, curtain_id: int) -> str:
	print(request.data)
	return request.data