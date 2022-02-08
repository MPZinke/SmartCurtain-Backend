#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.02.07                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


class Route:
	def __init__(self, endpoint: str, function: callable, *methods: list):
		self._endpoint: str = endpoint;
		self._function: callable = function;
		self._methods: list = methods if(methods) else ["GET"];


	# Instead of @app.route decorator, adds a route to the server.
	# https://stackoverflow.com/a/40466535
	def add_to_server(self, server: object) -> None:
		server.add_url_rule(self._endpoint, self._endpoint, self._function, methods=self._methods);
