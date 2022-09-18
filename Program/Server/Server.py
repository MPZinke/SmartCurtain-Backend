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


from flask import Flask;
from flask_cors import CORS;
from typing import List;


from Server import Route;
from System import System;
from Utility.ZThread import ZWidget;


class Server(ZWidget):
	def __init__(self, system: System):
		ZWidget.__init__(self, "Server", system);

		self._app = Flask(__name__);

		self._cors = CORS(self._app);
		self._app.config['CORS_HEADERS'] = 'Content-Type';

		self.add(
		  [
		  	Route("/"),
			Route("/api"),
			Route("/api/v1.0"),
			Route("/api/v1.0/curtains"),
			Route("/api/v1.0/curtains/all"),

			Route("/api/v1.0/curtains/<int:curtain_id>", "GET", "PATCH"),
			Route("/api/v1.0/curtains/<int:curtain_id>/events"),
			Route("/api/v1.0/curtains/<int:curtain_id>/events/all"),
			Route("/api/v1.0/curtains/<int:curtain_id>/events/new", "POST"),
			# Route("/api/v1.0/curtains/<int:curtain_id>/events/<string:event_time>", "GET", "PATCH", "DELETE"),

			Route("/api/v1.0/curtains/<string:curtain_name>", "GET", "PATCH"),
			Route("/api/v1.0/curtains/<string:curtain_name>/events"),
			Route("/api/v1.0/curtains/<string:curtain_name>/events/all"),
			Route("/api/v1.0/curtains/<string:curtain_name>/events/new", "POST"),
			# Route("/api/v1.0/curtains/<string:curtain_name>/events/<string:event_time>", "GET", "PATCH", "DELETE"),

			Route("/api/v1.0/events"),
			Route("/api/v1.0/events/all"),
			Route("/api/v1.0/events/<int:event_id>", "GET", "PATCH", "DELETE"),
			Route("/api/v1.0/events/new", "POST"),

			Route("/api/v1.0/options"),
			Route("/api/v1.0/options/all"),
			Route("/api/v1.0/options/<int:option_id>"),
			Route("/api/v1.0/options/<string:option_name>")
		  ]
		);


	def add(self, routes: List[Route]) -> None:
		for route in routes:
			route.add_to_server(self._app, self._System);


	def debug(self, flag=True) -> None:
		self._app.debug = flag;


	def _loop_process(self) -> None:
		"""
		SUMMARY: Adds routes to server & class, and starts the server instance.
		DETAILS: Sets routes using hardcoded routes, functions & HTTP request methods. Calls the Flask::run method.
		"""
		self._app.run(host="0.0.0.0", port=8080);
