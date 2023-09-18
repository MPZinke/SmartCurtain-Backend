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


import mpzinke
import threading
from werkzeug.exceptions import Forbidden, HTTPException, Unauthorized


import Global
from Server import Routes
from SmartCurtain import SmartCurtain


class Server:
	def __init__(self, smart_curtain: SmartCurtain):
		self._SmartCurtain: SmartCurtain = smart_curtain

		self._thread = threading.Thread(name="Server", target=self)
		self._app = mpzinke.Server(name="SmartCurtain-Backend", version=Global.VERSION)

		self._app.route("/", Routes.GET, additional_args={mpzinke.Server: self._app})

		additional_args = {SmartCurtain: smart_curtain}

		self._app.route("/homes", Routes.homes.GET, additional_args=additional_args)
		self._app.route("/homes/<int:home_id>", Routes.homes.GET_home_id, additional_args=additional_args)
		self._app.route("/homes/<int:home_id>/structure", Routes.homes.GET_home_id_structure, additional_args=additional_args)
		self._app.route("/homes/<int:home_id>/rooms", Routes.homes.GET_home_id_rooms, additional_args=additional_args)
		self._app.route("/homes/<int:home_id>/curtains", Routes.homes.GET_home_id_curtains, additional_args=additional_args)
		self._app.route("/homes/<int:home_id>/events", Routes.homes.GET_home_id_events, additional_args=additional_args)

		self._app.route("/rooms", Routes.rooms.GET, additional_args=additional_args)
		self._app.route("/rooms/<int:room_id>", Routes.rooms.GET_room_id, additional_args=additional_args)
		self._app.route("/rooms/<int:room_id>/curtains", Routes.rooms.GET_room_id_curtains, additional_args=additional_args)
		self._app.route("/rooms/<int:room_id>/events", Routes.rooms.GET_room_id_events, additional_args=additional_args)

		self._app.route("/curtains", Routes.curtains.GET, additional_args=additional_args)
		# self._app.route("/curtains/<int:curtain_id>", Routes.curtains.GET_curtain_id, additional_args=additional_args)
		self._app.route("/curtains/<int:curtain_id>", Routes.curtains.GET_curtain_id, POST=Routes.curtains.POST, additional_args=additional_args)
		self._app.route("/curtains/<int:curtain_id>/events", Routes.curtains.GET_curtain_id_events, additional_args=additional_args)

		# self.route("/events")
		# self.route("/events/<int:event_id>")

		# self.route("/options")
		# self.route("/options/all")
		# self.route("/options/<int:option_id>")
		# self.route("/options/<string:option_name>")

	# ———————————————————————————————————————————————————— THREAD ———————————————————————————————————————————————————— #

	def __call__(self) -> None:
		"""
		SUMMARY: Adds routes to server & class, and starts the server instance.
		DETAILS: Sets routes using hardcoded routes, functions & HTTP request methods. Calls the Flask::run method.
		"""
		self._app(host="0.0.0.0", port=8001)


	def start(self) -> None:
		self._thread.start()
