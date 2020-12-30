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
from os import getcwd as __OS__getcwd;
from pathlib import Path as __pathlib__Path;
from sys import path as __SYS__path;
from time import sleep;

 # Add parent directory to path for testing purposes
if(__name__ == '__main__'): __SYS__path.append(str(__pathlib__Path(__OS__getcwd()).parent));
from Server.ServerGlobal import *;
from Class.ZWidget import ZWidget;
import Other.Logger as Logger;


class Server(ZWidget):
	# ———— ROUTES INCLUSION ————
	# https://stackoverflow.com/a/47562412
	from Server.Routes.Root import index, favicon, test;


	def __init__(self, system):
		ZWidget.__init__(self, "Server", 10000000);
		print(MAIN_HTML_DIR, STATIC_HTML_DIR);
		self._server = Flask(__name__, template_folder=MAIN_HTML_DIR, static_folder=STATIC_HTML_DIR);
		self._server.secret_key = self.random_keygen(64);
		self._System = system;


	# Instead of @app.route decorator, adds a route to the server.
	# https://stackoverflow.com/a/40466535
	def add_route(self, url, handler, methods=["GET"]):
		self._server.add_url_rule(url, url, handler, methods=methods);


	def debug(self, flag=True):
		self._server.debug = flag;


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
	def _loop_process(self, **kw_args):
		routes = {"/" : [self.index, ["GET", "POST"]], "/favicon" : [self.favicon], "/test" : [self.test]};
		for route in routes: self.add_route(route, *routes[route]);

		self._server.run(host="0.0.0.0");


def main():
	server = Server();

	# server.debug();
	server.start();


if __name__ == '__main__':
	main()
