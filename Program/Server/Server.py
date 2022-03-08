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
from pathlib import Path;
import sys;
from time import sleep;


 # Add parent directory to path for testing purposes
if(__name__ == '__main__'): sys.path.append(str(Path(__file__).parent.parent));
from Server.ServerGlobal import *;

import Utility.Logger as Logger;
from Utility.WebSite import Header, Route;
from Utility.ZThread import ZWidget;


class Server(ZWidget):
	# ———— ROUTES INCLUSION ————
	# https://stackoverflow.com/a/47562412
	from Server.Routes.Root import index, index_POST, edit, events, events_POST, new, new_GET, new_POST, favicon;

	from Server.Routes.Advanced import advanced_logs;
	from Server.Routes.Advanced import advanced_log__log_filename;

	from Server.Routes.Api import api_update_deactivateevent;  # LEGACY
	from Server.Routes.Api import api_curtains__id__is_activated;
	from Server.Routes.Api import api_curtains__id__events_new;
	from Server.Routes.Api import api_curtains__id__events_new_now;
	from Server.Routes.Api import api_curtains__id__events_new_now_close;
	from Server.Routes.Api import api_curtains__id__events_new_now_open;
	from Server.Routes.Api import api_curtains__id__deactivate;
	from Server.Routes.Api import api_curtains__id__is_activated__is_activated;
	# from Server.Routes.Api import api_create_future;
	# from Server.Routes.Api import api_create_now;
	# from Server.Routes.Api import api_update_deactivateevent;
	# from Server.Routes.Api import api_update_deactivatecurtain;
	# from Server.Routes.Api import api_update_invalidateevent;


	def __init__(self, System):
		ZWidget.__init__(self, "Server", System);

		self._Server = Flask(__name__, template_folder=MAIN_HTML_DIR, static_folder=STATIC_HTML_DIR);
		self._Server.secret_key = self.random_keygen(64);

		self._header = None;

		self._routes =	[
		  Route("/", self.index, "GET", "POST"),
		  Route("/edit", self.edit),
		  Route("/events", self.events, "GET", "POST"),
		  Route("/new", self.new, "GET", "POST"),
		  Route("/favicon", self.favicon),
		  # Advanced
		  Route("/advanced/logs", self.advanced_logs),
		  Route("/advanced/log/<string:log_filename>", self.advanced_log__log_filename),
		  # API
		  # API::LEGACY
		  Route("/api/update/deactivateevent", self.api_update_deactivateevent, "POST"),
		  # API::CURRENT
		  # Route("/api", self., "GET"),  # Docs
		  # Route("/api/curtains", self., "GET"),  # Docs
		  # Route("/api/curtains/<int:curtain_id>", self., "GET"),
		  # Route("/api/curtains/<int:curtain_id>/events", self., "GET"),
		  Route("/api/curtains/<int:curtain_id>/is_activated", self.api_curtains__id__is_activated, "POST"),
		  # Route("/api/curtains/<int:curtain_id>/events/<int:event_id>", self., "GET"),
		  # Route("/api/curtains/<int:curtain_id>/events/<int:event_id>/kill", self., "DELETE"),
		  Route("/api/curtains/<int:curtain_id>/events/new", self.api_curtains__id__events_new, "POST"),
		  Route("/api/curtains/<int:curtain_id>/events/new/now", self.api_curtains__id__events_new_now, "POST"),
		  Route("/api/curtains/<int:curtain_id>/events/new/now/close", self.api_curtains__id__events_new_now_close, "POST"),
		  Route("/api/curtains/<int:curtain_id>/events/new/now/open", self.api_curtains__id__events_new_now_open, "POST"),
		  Route("/api/curtains/<int:curtain_id>/deactivate", self.api_curtains__id__deactivate, "PATCH"),
		  Route("/api/curtains/<int:curtain_id>/is_activated/<int:is_activated>", self.api_curtains__id__is_activated__is_activated, "PATCH"),
		];
		self.add_routes();


	def add_routes(self) -> None:
		for route in self._routes:
			route.add_to_server(self._Server);


	def debug(self, flag=True) -> None:
		self._Server.debug = flag;


	def set_session_and_header(self) -> None:
		if("_CURTAIN_current" not in session):
			session["_CURTAIN_current"] = 1;
		elif(request.method == "POST" and "__WRAPPER__curtain_select" in request.form):
			session["_CURTAIN_current"] = try_convert(request.form["__WRAPPER__curtain_select"], int, 1);

		self._header = Header(self._System);


	# Randomly create a key to secure the session using ASCII characters.
	# Takes the number of characters the session variable should be.
	# Uses random to get an index of a hardcoded ascii_character string.
	# Returns random key.
	def random_keygen(self, length) -> str:
		from random import randint
		ascii_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|" \
		  + "}~ \t\n\r\x0b\x0c"; 
		return "".join([ascii_chars[randint(0, len(ascii_chars)-1)] for x in range(length)]);


	# Adds routes to server & class, and starts the server instance.
	# Sets routes using hardcoded routes, functions & HTTP request methods.
	# Calls the Flask::run method.
	def _loop_process(self) -> None:
		self._Server.run(host="0.0.0.0", port=80);
