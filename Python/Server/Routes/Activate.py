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
from json import dumps;


# /api/current/
def api_activate(self):
	if("curtain" not in request.form): return "ERROR: NO CURTAIN ID SUPPLIED";
	current_event = self._System.Curtain(Curtains_id).current_event();
	if(not current_event):
		return "{\"curtain\" : 0, \"event\" : 0, \"current position\" : 0, \"length\" : 0, \"desired position\" : 0}"; 

	#TODO: pull values, send as JSON


# /api/complete/
def api_complete(self):
	if("data" not in request.form): pass;
	#TODO: get data from JSON
	return "SUCCESS";


# —————————————————————————————————————————————————————— BUILDERS ——————————————————————————————————————————————————————


