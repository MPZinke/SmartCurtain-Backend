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

from Global import *;
from Python.Class.Curtains import Curtains;
from Server import CNX, CURSOR, Server;


@Server.route("/activate", methods=["POST"])
def activate():
	if("_CURTAIN_current" not in session): return {"error" : "No curtain set"}.json();
	curtain_id = session["_CURTAIN_current"];
	if("_ACTIVATE_full_open" in request.form): return Curtains(curtain_id).open(CNX, CURSOR);
	return {};




# —————————————————————————————————————————————————————— BUILDERS ——————————————————————————————————————————————————————


