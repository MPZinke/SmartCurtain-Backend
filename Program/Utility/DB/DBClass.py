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
from json import dumps;
from typing import Any, List, Type, Union;
import inspect


from Utility.DB.AttributeType import AttributeType;
from Utility.DB.AttributeValue import AttributeValue;
import Utility.DB.DBFunctions as DBFunctions;



class DBClass:
	def __init__(self, db_prefix, **table_values: dict):
		for attribute in table_values:
			attribute_name = "_" + attribute.replace(".", "_");
			method_name = attribute.replace(".", "_");
			setattr(self, attribute_name, table_values[attribute] if table_values[attribute] else 0);
			setattr(self, method_name, self._get_or_set_attribute(db_prefix, attribute_name));

		self.attribute_types: List[AttributeType] = [];


	# Helper function for managing what happens to DB data & attributes.
	# Take the name of the attribute that is affected & that setting value (if being set).
	# Sets a new value if a new value is passed.
	# Will return the original value if no new value is passed. Returns whether new value successfully set.
	def _get_or_set_attribute(self, db_prefix: str, attribute_name: str) -> callable:
		def function(new_value: Any=None) -> bool:
			if(new_value is None):
				return getattr(self, attribute_name);

			if(new_value == getattr(self, attribute_name)):
				return True;  # values match, take the easy way out

			# Gotta update DB to match structure
			DB_function = getattr(DBFunctions, db_prefix+attribute_name);
			if((database_is_updated_flag := DB_function(self._id, new_value))):
				setattr(self, attribute_name, new_value);

			return database_is_updated_flag

		return function;

	# ——————————————————————————————————————————————————— UTILITY  ——————————————————————————————————————————————————— #

	def try_call(self, function: callable, *params: list, default: Union[Any, None]=None) -> Union[Any, None]:
		try:
			return function(*params)
		except:
			return default;


	# —————————————————————————————————————————————————— CONVERSION —————————————————————————————————————————————————— #


	def __iter__(self, *additional_args: list) -> dict:
		keys: list = [attribute.name() for attribute in self.attribute_types] + [arg for arg in additional_args];

		object_dict = {key: getattr(self, key) for key in keys};  # Get attrs
		object_dict = {};
		for key in keys:
			value = getattr(self, key);
			if(isinstance(value, DBClass)):
				value = dict(value);
			elif(isinstance(value, list)):
				value = [dict(val) if(isinstance(val, DBClass)) else val for val in value];

			object_dict[key[1:] if(key[0] == "_") else key] = value;

		yield from object_dict.items();


	def __repr__(self) -> str:
		return str(self);


	def __str__(self) -> str:
		return dumps(dict(self), default=str);


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

		for attribute_type in attribute_types:
			attribute_value: AttributeValue = self(attribute_type.name(), AttributeValue);
			if(attribute_type != attribute_value):
				key: str = attribute_type.name();
				value: Any = attribute_value.value();
				value_type_name: str = type(attribute_value.value()).__name__;
				required_type_name: str = attribute_type.allowed_types();
				raise TypeError(f"'{key}' value {value}, type: {value_type_name} is not of type {required_type_name}");


	@staticmethod
	def validate_values(attribute_types: List[AttributeType], attribute_values: List[AttributeValue]):
		for attribute_type in attribute_types:
			# Get attribute_value for the attribute_type
			corresponding_attribute_values: List[AttributeValue] = [];
			for attribute_value in attribute_values:
				if(attribute_value.name() == attribute_type.name()):
					corresponding_attribute_values.append(attribute_value);
			if(len(corresponding_attribute_values) == 0):
				raise TypeError(f"attribute_types are missing attribute: {attribute_value.name()}");

			attribute_value: AttributeValue = corresponding_attribute_values[0];
			if(attribute_type != attribute_value):
				key: str = attribute_type.name();
				value: Any = attribute_value.value();
				value_type_name: str = type(attribute_value.value()).__name__;
				required_type_name: str = attribute_type.allowed_types();
				raise TypeError(f"'{key}' value {value}, type: {value_type_name} is not of type {required_type_name}");
