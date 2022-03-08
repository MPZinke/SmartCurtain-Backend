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


from Global import *;


MAIN_HTML_DIR = PYTHON_DIR+"/Server/HTML/Root";
STATIC_HTML_DIR = PYTHON_DIR+"/Server/HTML/Static";


def add_error_and_redirect(error_message: str, redirect_url: str) -> str:
	session["error"] = error_message;
	return redirect(redirect_url);


def get_posted_value(*args)-> list:
	return [request.form[value] for value in args];


def posted(post : str) -> bool:
	return post in request.form;
