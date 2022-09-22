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


from flask import Flask, jsonify;
from flask_cors import CORS;
import traceback;
from typing import List;
from werkzeug.exceptions import HTTPException


from Server import Route;
from System import System;
from Utility.ZThread import ZWidget;


class Server(ZWidget):
	def __init__(self, system: System):
		ZWidget.__init__(self, "Server", system);

		self._app = Flask(__name__);

		self._cors = CORS(self._app);
		self._app.config['CORS_HEADERS'] = 'Content-Type';
		self._app.register_error_handler(Exception, self.handle_error)

		self._routes: List[Route] = [];

		self.route("/");
		self.route("/api");
		self.route("/api/v1.0");
		self.route("/api/v1.0/curtains");
		self.route("/api/v1.0/curtains/all");

		self.route("/api/v1.0/curtains/<int:curtain_id>", "GET", "PATCH");
		self.route("/api/v1.0/curtains/<int:curtain_id>/events");
		self.route("/api/v1.0/curtains/<int:curtain_id>/events/all");
		self.route("/api/v1.0/curtains/<int:curtain_id>/events/new", "POST");
		# self.route("/api/v1.0/curtains/<int:curtain_id>/events/<string:event_time>", "GET", "PATCH", "DELETE");

		self.route("/api/v1.0/curtains/<string:curtain_name>", "GET", "PATCH");
		self.route("/api/v1.0/curtains/<string:curtain_name>/events");
		self.route("/api/v1.0/curtains/<string:curtain_name>/events/all");
		self.route("/api/v1.0/curtains/<string:curtain_name>/events/new", "POST");
		# self.route("/api/v1.0/curtains/<string:curtain_name>/events/<string:event_time>", "GET", "PATCH", "DELETE");

		self.route("/api/v1.0/events");
		self.route("/api/v1.0/events/all");
		self.route("/api/v1.0/events/<int:event_id>", "GET", "PATCH", "DELETE");
		self.route("/api/v1.0/events/new", "POST");

		self.route("/api/v1.0/options");
		self.route("/api/v1.0/options/all");
		self.route("/api/v1.0/options/<int:option_id>");
		self.route("/api/v1.0/options/<string:option_name>");


	def add(self, routes: List[Route]) -> None:
		for route in routes:
			route.add_to_server(self._app, self._System);


	def debug(self, flag=True) -> None:
		self._app.debug = flag;


	def handle_error(self, error):
		"""
		FROM: https://readthedocs.org/projects/pallet/downloads/pdf/latest/
		 AND: https://stackoverflow.com/a/29332131
		"""
		if isinstance(error, HTTPException):
			return jsonify(error=str(error)), error.code;

		try:
			exception_traceback = traceback.format_exc();
		except:
			exception_traceback = "Unknown traceback";

		return jsonify(error=str(error), traceback=exception_traceback), 500;



	def _loop_process(self) -> None:
		"""
		SUMMARY: Adds routes to server & class, and starts the server instance.
		DETAILS: Sets routes using hardcoded routes, functions & HTTP request methods. Calls the Flask::run method.
		"""
		self._app.run(host="0.0.0.0", port=8080);


	def route(self, endpoint: str, *methods: list) -> None:
		route = Route(self._app, self._System, endpoint, *methods);
		route.add_to_server();
		self._routes.append(route);
