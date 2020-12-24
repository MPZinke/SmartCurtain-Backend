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


from flask import render_template, request, session;
from os import getcwd as __OS_getcwd;
from pathlib import Path;
import sys;


PROJECT_DIR = str(Path(__OS_getcwd()));
MAIN_HTML_DIR = PROJECT_DIR+"/HTML/Root";
STATIC_HTML_DIR = PROJECT_DIR+"/HTML/Static";


DB_USER = "root";
DB_PASSWORD = "mysql";
DATABASE = "SmartCurtain";
