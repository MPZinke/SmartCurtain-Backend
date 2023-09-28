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
		self._app = mpzinke.Server(name="SmartCurtain-Backend", version=Global.VERSION,
			additional_args={SmartCurtain: smart_curtain}
		)

		self._app.route("/", Routes.GET, additional_args={mpzinke.Server: self._app})

		self._app.route("/homes", Routes.homes.GET)
		self._app.route("/homes/<int:home_id>", Routes.homes.GET_home_id)
		self._app.route("/homes/<int:home_id>/rooms", Routes.homes.GET_home_id_rooms)
		self._app.route("/homes/<int:home_id>/curtains", Routes.homes.GET_home_id_curtains)
		self._app.route("/homes/<int:home_id>/events", Routes.homes.GET_home_id_events)

		self._app.route("/rooms", Routes.rooms.GET)
		self._app.route("/rooms/<int:room_id>", Routes.rooms.GET_room_id)
		self._app.route("/rooms/<int:room_id>/curtains", Routes.rooms.GET_room_id_curtains)
		self._app.route("/rooms/<int:room_id>/events", Routes.rooms.GET_room_id_events)
		self._app.route("/rooms/<int:room_id>/structure", Routes.rooms.GET_room_id_structure)

		self._app.route("/curtains", Routes.curtains.GET)
		self._app.route("/curtains/<int:curtain_id>", Routes.curtains.GET_curtain_id)
		self._app.route("/curtains/<int:curtain_id>/events", GET=Routes.curtains.GET_curtain_id_events,
			POST=Routes.curtains.POST_curtain_id_events
		)
		self._app.route("/curtains/<int:curtain_id>/structure", Routes.curtains.GET_curtain_id_structure)

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
