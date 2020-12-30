#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.23                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################



from flask import redirect, render_template, request, session;

from Class.Header import Header;
from Server.ServerGlobal import *;
from Server.ServerGlobal import set_session;


# —————————————————————————————————————————————————————— UTILITY ——————————————————————————————————————————————————————

def posted(post : str) -> bool:
	return post in request.form;


# ——————————————————————————————————————————————————————— ROUTES ———————————————————————————————————————————————————————

def index(self):
	set_session();
	header = Header(self._System);
	if(request.method == "POST"):
		curtain = header.selected_curtain();
		if(posted("open_button")): curtain.open(cnx, cursor);
		elif(posted("close_button")): curtain.close(cnx, cursor);
		elif(posted("set_button")):
			print(int(request.form["desired_position_input"]))
			curtain.open_percentage(cnx, cursor, desired_position=int(request.form["desired_position_input"]));
		return redirect("/");

	return render_template(MAIN_HTML_DIR+"/Home.html", header=header, session=session);


def favicon(self):
	return "";


def test(self):
	return "It worked"


# —————————————————————————————————————————————————————— BUILDERS ——————————————————————————————————————————————————————


