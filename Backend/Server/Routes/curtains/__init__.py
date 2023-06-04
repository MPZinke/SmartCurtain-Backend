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


from flask import request
import json
from werkzeug.exceptions import NotFound


from SmartCurtain import SmartCurtain


def GET(smart_curtain: SmartCurtain):
	"""
	`GET /curtains`
	"""
	return json.dumps({curtain.id(): curtain.name() for curtain in smart_curtain["-"]["-"]}, indent=4)


def GET_curtain_id(smart_curtain: SmartCurtain, curtain_id: int):
	"""
	`GET /curtains/<int:curtain_id>`
	"""
	if((curtain := smart_curtain["-"]["-"][curtain_id]) is None):
		raise NotFound(f"No curtain with id '{curtain_id}' was found")

	return json.dumps(dict(curtain), indent=4)


def GET_curtain_id_events(smart_curtain: SmartCurtain, curtain_id: int):
	"""
	`GET /curtains/<int:curtain_id>/events`
	"""
	if((curtain := smart_curtain["-"]["-"][curtain_id]) is None):
		raise NotFound(f"No curtain with id '{curtain_id}' was found")

	return json.dumps([dict(event) for event in curtain.CurtainEvents()], indent=4)


def POST(smart_curtain: SmartCurtain):
	pass
