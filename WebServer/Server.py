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
from sys import path as __SYS_path;
from time import sleep

from Global import *;
from Python.DB.DBFunctions import __CONNECT__;
from Python.Class.Header import Header;
import Python.Other.Logger as Logger;


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
# ———— DB SETUP ————
CNX, CURSOR = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);


# ———— ROUTES INCLUSION ————
from Routes.Root import *;
from Routes.State import *;


def main():
	Server.debug = True;
	Server.run();


if __name__ == '__main__':
	main()
