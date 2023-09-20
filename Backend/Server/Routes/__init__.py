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
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from flask import Response
import json
from mpzinke import Server


from Server.Routes import homes
from Server.Routes import rooms
from Server.Routes import curtains
from SmartCurtain import SmartCurtain


# `GET /`
def GET(server: Server) -> str:
	"""
	Lists all all backend endpoints.
	"""
	# Uses `json.dumps` to keep order
	return Response(json.dumps(dict(server)), mimetype="application/json")
