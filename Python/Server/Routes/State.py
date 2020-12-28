#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.26                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################



from flask import Blueprint, redirect, render_template, request, session;

from Class.Curtains import Curtains;
from DB.DBCredentials import *;
from DB.DBFunctions import __CONNECT__, ALL_Curtain_info;
from Server import Server;


# —————————————————————————————————————————————————————— UTILITY ——————————————————————————————————————————————————————


# ——————————————————————————————————————————————————————— ROUTES ———————————————————————————————————————————————————————

@Server.route("/state/<int:curtain_id>", methods=["POST"])
def state(curtain_id):
	cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
	curtain_info = ALL_Curtain_info(cursor, curtain_id);
	cursor.close();

	if(not curtain_info[0]): return {"error"};
	curtain = Curtains(*curtain_info);

	if("current_position_percent__is_activated" in request.form):
		return curtain.json(["is_activated", "current_position_percent_int"]);
