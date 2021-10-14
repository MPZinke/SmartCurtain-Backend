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
from pathlib import Path as __pathlib__Path;
from sys import path as __SYS__path;
from time import sleep;

 # Add parent directory to path for testing purposes
if(__name__ == '__main__'): __SYS__path.append(str(__pathlib__Path(__file__).parent.parent));
from Server.ServerGlobal import *;
from Other.Class.ZWidget import ZWidget;
import Other.Logger as Logger;


class Server(ZWidget):
	# ———— ROUTES INCLUSION ————
	# https://stackoverflow.com/a/47562412
	from Server.Routes.Root import index, edit, events, new, favicon, test;
	from Server.Routes.State import state;
	from Server.Routes.Api import api_create_future;
	from Server.Routes.Api import api_create_now;
	from Server.Routes.Api import api_update_deactivateevent;
	from Server.Routes.Api import api_update_deactivatecurtain;


	def __init__(self, System):
		ZWidget.__init__(self, "Server", System);

		self._Server = Flask(__name__, template_folder=MAIN_HTML_DIR, static_folder=STATIC_HTML_DIR);
		self._Server.secret_key = self.random_keygen(64);
		self.add_routes();


	# Instead of @app.route decorator, adds a route to the server.
	# https://stackoverflow.com/a/40466535
	def add_route(self, url, handler, methods=["GET"]):
		self._Server.add_url_rule(url, url, handler, methods=methods);


	def add_routes(self):
		routes =	{
						"/" : [self.index, ["GET", "POST"]],
						"/edit" : [self.edit],
						"/events" : [self.events],
						"/new" : [self.new, ["GET", "POST"]],
						"/favicon" : [self.favicon],
						"/test" : [self.test, ["GET", "POST"]],
						"/state/<int:Curtains_id>" : [self.state, ["POST"]],
						"/api/create/future" : [self.api_create_future, ["POST"]],
						"/api/create/now" : [self.api_create_now, ["POST"]],
						"/api/update/deactivateevent" : [self.api_update_deactivateevent, ["POST"]],
						"/api/update/deactivatecurtain" : [self.api_update_deactivatecurtain, ["POST"]]
					};
		for route in routes: self.add_route(route, *routes[route]);


	def debug(self, flag=True):
		self._Server.debug = flag;


	# Randomly create a key to secure the session using ASCII characters.
	# Takes the number of characters the session variable should be.
	# Uses random to get an index of a hardcoded ascii_character string.
	# Returns random key.
	def random_keygen(self, length):
		from random import randint
		ascii_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|" \
		  + "}~ \t\n\r\x0b\x0c"; 
		return "".join([ascii_chars[randint(0, len(ascii_chars)-1)] for x in range(length)]);


	# Adds routes to server & class, and starts the server instance.
	# Sets routes using hardcoded routes, functions & HTTP request methods.
	# Calls the Flask::run method.
	def _loop_process(self):
		self._Server.run(host="0.0.0.0", port=80);
