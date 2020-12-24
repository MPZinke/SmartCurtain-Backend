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
from flask_mysql_connector import MySQL;

from Global import *;
from Global import set_session;
from Python.Class.Header import Header;
from Server import _MYSQL_, Server;


@Server.route("/", methods=["GET", "POST"])
def index():
	set_session();
	curtain_id = session["_CURTAIN_current"];
	header = Header(_MYSQL_.new_cursor(buffered=True, dictionary=True), curtain_id);
	return render_template("Home.html", header=header, session=session);


@Server.route("/favicon.ico", methods=["GET"])
def favicon():
	return "";


@Server.route("/test")
def test():
	return "It worked"


# —————————————————————————————————————————————————————— BUILDERS ——————————————————————————————————————————————————————


