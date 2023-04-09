#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.09.03                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import json;


from SmartCurtain import SmartCurtain;


# `GET /api/v1.0/curtains/<string:curtain_name>/events/all`
# Lists all events for a curtain.
def GET(smart_curtain: SmartCurtain, curtain_name: str):
	if((curtain := smart_curtain.Curtain(name=curtain_name)) is None):
		raise Exception("Not found");  #TODO

	return json.dumps([dict(event) for event in curtain.CurtainEvents()], default=str);
