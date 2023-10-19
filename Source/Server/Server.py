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


import Global
from Server import Routes
from SmartCurtain import SmartCurtain, Home, Room, Curtain


class Server:
	def __init__(self, smart_curtain: SmartCurtain):
		self._SmartCurtain: SmartCurtain = smart_curtain

		self._thread = threading.Thread(name="Server", target=self)
		self._app = mpzinke.Server(name="SmartCurtain-Backend", version=Global.VERSION,
			additional_args={SmartCurtain: smart_curtain}
		)

		self._app.route("/", Routes.GET, additional_args={mpzinke.Server: self._app})

		self._app.route("/homes", Routes.GET_area[Home])
		self._app.route("/homes/<int:area_id>", Routes.GET_area_id[Home])
		self._app.route("/homes/<int:area_id>/structure", Routes.GET_area_id_structure[Home])
		self._app.route("/homes/<int:area_id>/events", GET=Routes.GET_area_id_events[Home],
			POST=Routes.POST_area_id_events[Home]
		)
		self._app.route("/homes/<int:area_id>/events/<int:event_id>", Routes.GET_area_id_event_id[Home])

		self._app.route("/rooms", Routes.GET_area[Room])
		self._app.route("/rooms/<int:area_id>", Routes.GET_area_id[Room])
		self._app.route("/rooms/<int:area_id>/structure", Routes.GET_area_id_structure[Room])
		self._app.route("/rooms/<int:area_id>/events", GET=Routes.GET_area_id_events[Room],
			POST=Routes.POST_area_id_events[Room]
		)
		self._app.route("/rooms/<int:area_id>/events/<int:event_id>", Routes.GET_area_id_event_id[Room])

		self._app.route("/curtains", Routes.GET_area[Curtain])
		self._app.route("/curtains/<int:area_id>", Routes.GET_area_id[Curtain])
		self._app.route("/curtains/<int:area_id>/structure", Routes.GET_area_id_structure[Curtain])
		self._app.route("/curtains/<int:area_id>/events", GET=Routes.GET_area_id_events[Curtain],
			POST=Routes.POST_area_id_events[Curtain]
		)
		self._app.route("/curtains/<int:area_id>/events/<int:event_id>",
			GET=Routes.GET_area_id_event_id[Curtain],
			PATCH=Routes.PATCH_area_id_event_id[Curtain],
			DELETE=Routes.DELETE_area_id_event_id[Curtain]
		)

		# self.route("/events")
		# self.route("/events/<int:event_id>")

		self._app.route("/options", Routes.GET_options)
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
