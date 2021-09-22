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
from typing import Union;

from Other.Global import *;


MAIN_HTML_DIR = SMARTCURTAIN_DIR+"/Server/HTML/Root";
STATIC_HTML_DIR = SMARTCURTAIN_DIR+"/Server/HTML/Static";


def add_error_and_redirect(error_message: str, redirect_url: str):
	session["error"] = error_message;
	return redirect(redirect_url);


def get_posted_value(*args)-> list:
	return [request.form[value] for value in args];


def posted(post : str) -> bool:
	return post in request.form;


def set_session():
	if("_CURTAIN_current" not in session): session["_CURTAIN_current"] = 1;
	elif(request.method == "POST" and "__WRAPPER__curtain_select" in request.form):
		try: session["_CURTAIN_current"] = int(request.form["__WRAPPER__curtain_select"]);
		except: session["_CURTAIN_current"] = 1;  # naughty stuff posted: default to 1