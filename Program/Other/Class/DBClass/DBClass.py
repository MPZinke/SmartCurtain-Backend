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
from typing import Any, List, Type, Union;


from Other.Class.DBClass.AttributeType import AttributeType;
from Other.Class.DBClass.AttributeValue import AttributeValue;
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


	def __call__(self, attribute_name: str, conversion_type: Type=AttributeType):
		if(not hasattr(self, attribute_name)):
			raise TypeError(f"DB Object is missing attribute: {attribute_name}");

		if(conversion_type == AttributeType):
			return AttributeType(attribute_name, type(getattr(self, attribute_name)));

		elif(conversion_type == AttributeValue):
			return AttributeValue(attribute_name, getattr(self, attribute_name));


	# Check key value types of dictonary for attributes to be passed to dictionary.
	def validate(self, attribute_types: Union[List[AttributeType], None]=None) -> None:
		if(attribute_types is None):
			attribute_types = self.attribute_types;

		print("I'M FREAKING SCREAMING AT YOU")
		print(attribute_types)
		for attribute_type in attribute_types:
			attribute_value: AttributeValue = self(attribute_type.name());
			if(attribute_type != attribute_value):
				print(f"Key: {key} is bad");
				key: str = attribute_type.name();
				value: Any = attribute_value.value();
				value_type_name: str = type(attribute_value.value()).__name__;
				required_type_name: str = attribute_type.allowed_types();
				raise TypeError(f"'{key}' value {value}, type: {value_type_name} is not of type {required_type_name}");
			print(f"Key: {key} is good");



	@staticmethod
	def validate_values(attribute_types: List[AttributeType], attribute_values: List[AttributeValue]):
		for attribute_type in attribute_types:
			# Get attribute_value for the attribute_type
			corresponding_attribute_values: List[AttributeValue] = [];
			for attribute_value in attribute_values:
				if(attribute_value.name() == attribute_type.name()):
					corresponding_attribute_value.append(attribute_value);
			if(not len(corresponding_attribute_values)):
				raise TypeError(f"attribute_types are missing attribute: {attribute_value.name()}");

			attribute_value: AttributeValue = corresponding_attribute_values[0];
			if(attribute_type != attribute_value):
				key: str = attribute_type.name();
				value: Any = attribute_value.value();
				value_type_name: str = type(attribute_value.value()).__name__;
				required_type_name: str = attribute_type.allowed_types();
				raise TypeError(f"'{key}' value {value}, type: {value_type_name} is not of type {required_type_name}");
