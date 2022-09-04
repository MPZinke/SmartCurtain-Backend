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
import inspect;
import os;
import re;
import types;
from typing import get_type_hints, List;


from Server import Root;
from System import System;


Module = types.ModuleType;  # typedef types.ModuleType


class Route:
	PARAM_REGEX = r"<(int|string):([_a-zA-Z][_a-zA-Z0-9]*)>"
	PARAM_NAME_REGEX = r"<(?:int|string):([_a-zA-Z][_a-zA-Z0-9]*)>";

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
		server.add_url_rule(self._endpoint+"/", self._endpoint+"/", endpoint_function, methods=self._methods);


	def callback_function(self, method: str) -> str:
		"""
		SUMMARY: Determines the callback function for the request method.
		"""
		callback_module = self.__module(Root, self.__module_path_parts());
		return self.__modules_method_function(method, callback_module);


	def __module(self, current_module: Module, path: list):
		"""
		SUMMARY: Gets the module down the path of the endpoint.
		"""
		if(len(path) == 0):
			return current_module;

		if(not hasattr(current_module, path[0].lower().replace('.', '_'))):
			raise Exception(f"Module not found: {path[0].lower().replace('.', '_')}");

		return self.__module(getattr(current_module, path[0].lower()), path[1:]);


	def __modules_method_function(self, method: str, module: Module) -> bool:
		"""
		SUMMARY: Gets the desired callback for the endpoint based on name, params, and module.
		"""
		endpoint_params = {param[1]: param[0] for param in re.findall(self.PARAM_REGEX, self._endpoint)};
		callback_params = {"system": System, **endpoint_params};

		module_function_tuples = [method for method in inspect.getmembers(module) if(inspect.isfunction(method[1]))];
		for function_name, function in module_function_tuples:
			function_params: dict = function.__annotations__;
			if(function_name != method or len(callback_params) != len(function_params)):
				continue;

			mapping = {"int": int, "string": str};
			if(all(mapping.get(type, type) == function_params[name] for name, type in callback_params.items())):
				return function;

		callback_param_str: str = ", ".join(callback_params.keys());
		raise Exception(f"No matching function for method '{method}' with params: '{callback_param_str}'" +
		  f" for module '{module.__name__}'");


	def __module_path_parts(self) -> List[str]:
		return [part.lower().replace('.', '_') for part in self.path_parts()];


	def path_parts(self) -> List[str]:
		"""
		SUMMARY: Gets the rescinding parts to a path starting at the root directory. 
		"""
		def is_param(part: str) -> bool:
			return re.fullmatch(self.PARAM_REGEX, part);

		if(self._endpoint == "/"):
			return [];

		parts = [part for part in os.path.normpath(self._endpoint).split(os.sep)];
		# [param name if(part is param) else part for part in parts]
		parts = [re.findall(self.PARAM_NAME_REGEX, part)[0] if(is_param(part)) else part for part in parts];
		return parts[int(self._endpoint[0] == '/'):];  # ignore empty '' if path starts with '/'
