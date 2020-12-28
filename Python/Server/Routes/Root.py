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



from flask import Blueprint, redirect, render_template, request, session;

from DB.DBCredentials import *;
from Class.Header import Header;
from Class.Curtains import Curtains;
from DB.DBFunctions import __CONNECT__;
from Server import Server;
from ServerGlobal import set_session;


# —————————————————————————————————————————————————————— UTILITY ——————————————————————————————————————————————————————

def posted(post : str) -> bool:
	return post in request.form;


# ——————————————————————————————————————————————————————— ROUTES ———————————————————————————————————————————————————————

@Server.route("/", methods=["GET", "POST"])
def index():
	set_session();
	curtain_id = session["_CURTAIN_current"];
	cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
	header = Header(cursor, curtain_id);
	if(request.method == "POST"):
		curtain = header.selected_curtain();
		if(posted("open_button")): curtain.open(cnx, cursor);
		elif(posted("close_button")): curtain.close(cnx, cursor);
		elif(posted("set_button")):
			print(int(request.form["desired_position_input"]))
			curtain.open_percentage(cnx, cursor, desired_position=int(request.form["desired_position_input"]));

		return redirect("/");

	cursor.close();
	return render_template("Home.html", header=header, session=session);


@Server.route("/favicon.ico", methods=["GET"])
def favicon():
	return "";


@Server.route("/test")
def test():
	return "It worked"


# —————————————————————————————————————————————————————— BUILDERS ——————————————————————————————————————————————————————


