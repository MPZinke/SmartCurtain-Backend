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


from flask import request, session;
from os import getcwd as __OS__getcwd;
from pathlib import Path as __pathlib__Path;
import sys;

from Other.Global import *;


SERVER_DIR = str(__pathlib__Path(__OS__getcwd()));
MAIN_HTML_DIR = SERVER_DIR+"/HTML/Root";
STATIC_HTML_DIR = SERVER_DIR+"/HTML/Static";


def set_session():
	if("_CURTAIN_current" not in session): session["_CURTAIN_current"] = 1;
	elif(request.method == "POST" and "__WRAPPER__curtain_select" in request.form):
		try: session["_CURTAIN_current"] = int(request.form["__WRAPPER__curtain_select"]);
		except: session["_CURTAIN_current"] = 1;  # naughty stuff posted: default to 1