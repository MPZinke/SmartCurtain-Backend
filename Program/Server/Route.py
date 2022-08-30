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
	PARAM_RE = r"<(int|string):([_a-zA-Z][_a-zA-Z0-9]*)>"

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

		endpoint = self.__prettified_endpoint();
		server.add_url_rule(endpoint, endpoint, endpoint_function, methods=self._methods);


	def callback_function(self, method: str) -> str:
		"""
		SUMMARY: 
		"""
		callback_module = self.__module(Root, self.__module_path_parts());
		return self.__module_function(method, callback_module);


	def __module(self, current_module: Module, path: list):
		"""
		SUMMARY: Gets the module down the path of the endpoint.
		"""
		if(len(path) < 2):
			return current_module;

		if(not hasattr(current_module, path[0].lower().replace('.', '_'))):
			raise Exception(f"Module not found: {path[0].lower().replace('.', '_')}");

		return self.__module(getattr(current_module, path[0].lower()), path[1:]);


	def __module_function(self, method: str, module: Module) -> bool:
		"""
		SUMMARY: Gets the desired callback for the endpoint based on name, params, and module.
		"""
		callback_name = f"{method}__{self.__module_path_parts()[-1]}";
		endpoint_params = {param[1]: param[0] for param in re.findall(self.PARAM_RE, self._endpoint)};
		callback_params = {"system": System, **endpoint_params};

		module_function_tuples = [method for method in inspect.getmembers(module) if(inspect.isfunction(method[1]))];
		for function_name, function in module_function_tuples:
			function_params: dict = function.__annotations__;
			if(function_name != callback_name or len(callback_params) != len(function_params)):
				continue;

			mapping = {"int": int, "string": str, System: System};
			if(all(mapping[type] == function_params[name] for name, type in callback_params.items())):
				return function;

		callback_param_str: str = ", ".join(callback_params.keys());
		raise Exception(f"No matching function named '{callback_name}' with params: '{callback_param_str}'" +
		  f" for module '{module.__name__}'");


	def __module_path_parts(self) -> List[str]:
		parts: List[str] = [part for part in self.path_parts() if(part and not re.match(self.PARAM_RE, part))];
		return [part.lower().replace('.', '_') for part in parts];


	def __prettified_endpoint(self) -> str:
		"""
		SUMMARY: Removes "index" from path
		"""
		print(os.path.join("/", *[part for part in self.path_parts() if(part != "index")]));
		return os.path.join("/", *[part for part in self.path_parts() if(part != "index")]);


	def path_parts(self) -> List[str]:
		return [part for part in os.path.normpath(self._endpoint).split(os.sep)];
