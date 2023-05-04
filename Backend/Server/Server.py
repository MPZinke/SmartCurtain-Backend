#!/opt/homebrew/bin/python3
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


from flask import Flask, jsonify
from flask_cors import CORS
import threading
import traceback
from typing import List
from werkzeug.exceptions import HTTPException


from Server import Route
from SmartCurtain import SmartCurtain


class Server:
	def __init__(self, smart_curtain: SmartCurtain):
		self._thread = threading.Thread(name="Server", target=self)

		self._SmartCurtain: SmartCurtain = smart_curtain

		self._app = Flask(__name__)

		self._cors = CORS(self._app)
		self._app.config['CORS_HEADERS'] = 'Content-Type'
		self._app.register_error_handler(Exception, self.handle_error)

		self._routes: List[Route] = []

		self.route("/", secure=False)
		self.route("/api", secure=False)
		self.route("/api/v1.0", secure=False)
		self.route("/api/v1.0/curtains", secure=False)
		self.route("/api/v1.0/curtains/all")

		self.route("/api/v1.0/curtains/<int:curtain_id>", "GET", "PATCH")
		self.route("/api/v1.0/curtains/<int:curtain_id>/events")
		self.route("/api/v1.0/curtains/<int:curtain_id>/events/all")
		self.route("/api/v1.0/curtains/<int:curtain_id>/events/new", "POST")
		# self.route("/api/v1.0/curtains/<int:curtain_id>/events/<string:event_time>", "GET", "PATCH", "DELETE")

		self.route("/api/v1.0/curtains/<string:curtain_name>", "GET", "PATCH")
		self.route("/api/v1.0/curtains/<string:curtain_name>/events")
		self.route("/api/v1.0/curtains/<string:curtain_name>/events/all")
		self.route("/api/v1.0/curtains/<string:curtain_name>/events/new", "POST")
		# self.route("/api/v1.0/curtains/<string:curtain_name>/events/<string:event_time>", "GET", "PATCH", "DELETE")

		self.route("/api/v1.0/events")
		self.route("/api/v1.0/events/all")
		self.route("/api/v1.0/events/<int:event_id>", "GET", "PATCH", "DELETE")
		self.route("/api/v1.0/events/new", "POST")

		self.route("/api/v1.0/options")
		self.route("/api/v1.0/options/all")
		self.route("/api/v1.0/options/<int:option_id>")
		self.route("/api/v1.0/options/<string:option_name>")

	# ———————————————————————————————————————————————————— THREAD ———————————————————————————————————————————————————— #

	def __call__(self) -> None:
		"""
		SUMMARY: Adds routes to server & class, and starts the server instance.
		DETAILS: Sets routes using hardcoded routes, functions & HTTP request methods. Calls the Flask::run method.
		"""
		self._app.run(host="0.0.0.0", port=8080)


	def start(self) -> None:
		self._thread.start()


	def debug(self, flag=True) -> None:
		self._app.debug = flag


	def handle_error(self, error):
		"""
		SUMMARY: Handles the return response for any server error that occurs during a request.
		PARAMS:  Takes the error that has occured.
		FROM: https://readthedocs.org/projects/pallet/downloads/pdf/latest/
		 AND: https://stackoverflow.com/a/29332131
		"""
		if isinstance(error, HTTPException):
			return jsonify(error=str(error)), error.code

		try:
			exception_traceback = traceback.format_exc()
		except:
			exception_traceback = "Unknown traceback"

		return jsonify(error=str(error), traceback=exception_traceback), 500


	def route(self, endpoint: str, *methods: list, secure: bool=True) -> None:
		"""
		SUGAR:  Makes a cleaner version to add a Route to the Flask server.
		PARAMS: Takes the endpoint to route, the request methods to accept, whether the route requires authorization.
		"""
		route = Route(self._app, self._SmartCurtain, endpoint, *methods, secure=secure)
		route.add_to_server()
		self._routes.append(route)
