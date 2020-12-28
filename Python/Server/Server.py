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


from flask import Flask, request, session;
from flask_mysql_connector import MySQL;
from json import dumps;
from os import getcwd as __OS__getcwd;
from pathlib import Path as __pathlib__Path;
from sys import path as __SYS__path;
from time import sleep

__SYS__path.append(str(__pathlib__Path(__OS__getcwd()).parent));  # Add parent directory to path
from ServerGlobal import *;
from DB.DBFunctions import __CONNECT__;
from Class.Header import Header;
import Other.Logger as Logger;


# randomly create a key to secure the session
def random_keygen(length):
	from random import randint
	ascii_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c"
	return "".join([ascii_chars[randint(0, 99)] for x in range(length)])


# used to print to console from Jinja2 script
def jinja2_print(text):
	print(text);
	return "";


# ———— SERVER SETUP ————
Server = Flask(__name__, template_folder=MAIN_HTML_DIR, static_folder=STATIC_HTML_DIR);
Server.secret_key = random_keygen(64);


# ———— ROUTES INCLUSION ————
from Routes.Root import *;
from Routes.State import *;


def main():
	Server.debug = True;
	Server.run(host="0.0.0.0");


if __name__ == '__main__':
	main()
