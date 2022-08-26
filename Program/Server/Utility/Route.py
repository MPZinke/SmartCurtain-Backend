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


from flask import request
import re;
from typing import List;


import Server.Routes.Api as Api;


class Route:
	def __init__(self, endpoint: str, *methods: List[str]):
		self._endpoint: str = endpoint;
		self._methods: List[str] = ["GET"] if(not methods) else methods;
		self._callbacks = {method: self.callback_function(method) for method in self._methods};
		# self._callback_methods: CallbackMethod = callback_methods;


	# Instead of @app.route decorator, adds a route to the server.
	# https://stackoverflow.com/a/40466535
	def add_to_server(self, server: object) -> None:
		def endpoint_function(*args: list, **kwargs: dict):  # server instead of self
			return self._callbacks[request.method](server, *args, **kwargs);

		server.add_url_rule(self._endpoint, self._endpoint, endpoint_function, methods=self._methods);


	def callback_function(self, method: str) -> str:
		endpoint: str = self._endpoint;
		endpoint = re.sub(r"<(string|int):", "", endpoint);
		endpoint = re.sub(r">", "", endpoint);
		endpoint = endpoint.replace(".", "_");
		endpoint = endpoint.replace("/", "__");

		return getattr(Api, f"{method}{endpoint}");


	def __str__(self):
		callback_str = ",".join([f"{method}: {callback.__name__}" for method, callback in self._callbacks.items()]);
		return f"{self._endpoint} {callback_str}";
