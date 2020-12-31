#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.26                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION: Get and set individual variables for a specific curtain.                                              #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################



from flask import redirect, render_template, request, session;
from json import dumps;


# —————————————————————————————————————————————————————— UTILITY ——————————————————————————————————————————————————————


# ——————————————————————————————————————————————————————— ROUTES ———————————————————————————————————————————————————————

# /state/<int:Curtains_id>
def state(self, Curtains_id : int):
	if(Curtains_id not in self._System.Curtains()): return {"error"};

	if("current_position_percent__is_activated" in request.form):
		print(self._System.Curtain(Curtains_id).dict(["is_activated", "current_position_percent_int"]));
		return dumps(self._System.Curtain(Curtains_id).dict(["is_activated", "current_position_percent_int"]));
