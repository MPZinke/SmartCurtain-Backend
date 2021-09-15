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
from Other.Logger import log_error;
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
		try:
			if(posted("open_button")): header.selected_curtain().open_immediately(header.selected_curtain().length());
			elif(posted("close_button")): header.selected_curtain().close_immediately();
			elif(posted("set_button")):
				position = int(request.form["desired_position_input"])
				header.selected_curtain().open_percentage(desired_position=position);
				session["success"] = "Successfully created event";
		except Exception as error:
			log_error(error);
			session["error"] = f"Error setting event {str(error)}";
		return redirect("/");

	return render_template("Home.html", header=header, session=session);


def events(self):
	set_session();
	header = Header(self._System);
	return render_template("Events.html", header=header, session=session);


def favicon(self):
	return "";


def test(self):
	print(request.get_json());
	return "{\"success\":\"It worked\"}"


# —————————————————————————————————————————————————————— BUILDERS ——————————————————————————————————————————————————————


