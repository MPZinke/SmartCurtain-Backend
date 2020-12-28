#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.25                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################



from flask import Blueprint, redirect, render_template, request, session;

from Class.Curtains import Curtains;
from DB.DBCredentials import *;
from DB.DBFunctions import __CONNECT__;
from Server import Server;


@Server.route("/activate", methods=["POST"])
def activate():
	cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
	if("_CURTAIN_current" not in session): return {"error" : "No curtain set"}.json();
	curtain_id = session["_CURTAIN_current"];
	if("_ACTIVATE_full_open" in request.form): return Curtains(curtain_id).open(CNX, CURSOR);
	return {};




# —————————————————————————————————————————————————————— BUILDERS ——————————————————————————————————————————————————————


