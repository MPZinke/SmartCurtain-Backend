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


from flask import Flask, request;
import os;
import re;
from typing import List;


from Server import Root;
from System import System;


class Route:
	def __init__(self, endpoint: str, *methods: List[str]):
		self._endpoint: str = endpoint;
		self._methods: List[str] = ["GET"] if(not methods) else methods;
		self._callbacks = {method: self.callback_function(method) for method in self._methods};


	def __str__(self):
		callback_str = ",".join([f"{method}: {callback.__name__}" for method, callback in self._callbacks.items()]);
		return f"{self._endpoint} {callback_str}";


	# Instead of @app.route decorator, adds a route to the server.
	# https://stackoverflow.com/a/40466535
	def add_to_server(self, server: Flask, system: System) -> None:
		def endpoint_function(*args: list, **kwargs: dict):  # system instead of self
			return self._callbacks[request.method](system, *args, **kwargs);

		server.add_url_rule(self._endpoint, self._endpoint, endpoint_function, methods=self._methods);


	def callback_function(self, method: str) -> str:
		def module(current_module, path: list):
			# Ignore "upcoming variables"
			while(len(path) and re.match(r"<(string|int):[_a-zA-Z][_a-zA-Z0-9]*", path[0])):
				path.pop();

			# Recurse down modules
			if(len(path) > 2):
				module_name = f"{path[0][0].upper()}{path[0][1:].lower()}";
				if(not hasattr(current_module, module_name)):
					return None;

				return module(getattr(current_module, module_name), path[1:]);

			return current_module;

		callback_module = module(Root, os.path.split(self._endpoint));
		callback_arguments = re.findall(r"<(string|int):[_a-zA-Z][_a-zA-Z0-9]*>", path[0])):
		for function in callback_module:
			function_params = 
			if()

		_, module, version = split(self._endpoint)[:3];
		print(split(self._endpoint))
		print("module: ", module, "version: ", version)

		endpoint: str = self._endpoint;
		endpoint = re.sub(r"<(string|int):", "", endpoint);
		endpoint = re.sub(r">", "", endpoint);
		endpoint = endpoint.replace(".", "_");
		endpoint = endpoint.replace("/", "__");

		return getattr(getattr(module.lower(), version.lower()), f"{method}{endpoint}");
