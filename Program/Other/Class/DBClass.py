#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.09.25                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import json;
from typing import Any, Union;


from Other.DB.DBCredentials import *;
import Other.DB.DBFunctions as DBFunctions;
from Other.DB.DBFunctions import __CLOSE__, __CONNECT__;



class DBClass:
	def __init__(self, db_prefix, **table_values: dict):
		for attribute in table_values:
			attribute_name = "_" + attribute.replace(".", "_");
			method_name = attribute.replace(".", "_");
			setattr(self, attribute_name, table_values[attribute] if table_values[attribute] else 0);
			setattr(self, method_name, self._get_or_set_attribute(db_prefix, attribute_name));


	# Helper function for managing what happens to DB data & attributes.
	# Take the name of the attribute that is affected & that setting value (if being set).
	# Sets a new value if a new value is passed.
	# Will return the original value if no new value is passed. Returns whether new value successfully set.
	def _get_or_set_attribute(self, db_prefix: str, attribute_name: str):
		def function(new_value=None):
			if(isinstance(new_value, type(None))):
				return getattr(self, attribute_name);

			if(new_value == getattr(self, attribute_name)):
				return True;  # values match, take the easy way out

			# gotta update DB to match structure
			DB_function = getattr(DBFunctions, db_prefix+attribute_name);
			cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
			success_flag = DB_function(cnx, cursor, self._id, new_value);

			if(success_flag): setattr(self, attribute_name, new_value);

			return success_flag + bool(__CLOSE__(cnx, cursor));

		return function;

	# ——————————————————————————————————————————————————— UTILITY  ——————————————————————————————————————————————————— #

	def try_call(self, function: callable, *params: list, default: Union[Any, None]=None) -> Union[Any, None]:
		try:
			return function(*params)
		except:
			return default;


	# —————————————————————————————————————————————————— CONVERSION —————————————————————————————————————————————————— #

	def dict(self) -> dict:
		return {attr : getattr(self, attr) for attr in self.__dict__};


	def __str__(self):
		attribute_dict = {key: value for key, value in self.dict().items() if(key[0] == "_")};
		str_dict = {key: str(value) if(isinstance(value, object)) else value for key, value in attribute_dict.items()};
		return self.try_call(json.dumps, str_dict, default="");


	# Check key value types of dictonary for attributes to be passed to dictionary.
	@staticmethod
	def validate_data(keys: list, types: list, values: dict) -> None:
		for key in keys:
			if(key not in values):
				raise Exception(f"Missing argument: {key}");

		if(len(keys) != len(types)):
			raise Exception("Length of keys does not equal length of types");

		for x in range(len(keys)):
			value = values[keys[x]];
			type_list = types[x] if(isinstance(types[x], list)) else [types[x]];
			
			if(any(isinstance(value, t) for t in type_list)): continue

			key = keys[x];
			value_type_name = type(value).__name__;
			required_type_name = " or".join([t.__name__ for t in type_list]);
			raise TypeError(f"'{key}' value {value}, type: {value_type_name} is not of type {required_type_name}");
