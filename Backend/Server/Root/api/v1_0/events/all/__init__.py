#!/usr/bin/env python3
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


import Server.Root.api.v1_0.events.all;
from SmartCurtain import SmartCurtain;


def GET(smart_curtain: SmartCurtain):
	return json.dumps([dict(event) for curtain in smart_curtain.Curtains() for event in curtain.CurtainEvents()],
	  default=str);
