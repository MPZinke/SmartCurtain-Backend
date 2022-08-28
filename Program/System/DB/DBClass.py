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


from System.DB.AttributeType import AttributeType;
import System.DB.DBFunctions as DBFunctions;



class DBClass:
	def __init__(self, db_prefix, **table_values: dict):
		for attribute in table_values:
			method_name = attribute.replace(".", "_");
			attribute_name = "_" + method_name;
			setattr(self, attribute_name, table_values[attribute] if(table_values[attribute]) else 0);
			setattr(self, method_name, self.__getter_setter_method(db_prefix, attribute_name, method_name));

		self.attribute_types: List[AttributeType] = [];


	def __getter_setter_method(self, db_prefix: str, attribute_name: str, method_name: str) -> callable:
		"""
		SUMMARY: Creates a method for Getting/Setting a DB attribute.
		PARAMS:  Takes the prefix for the DB operation, the variable name of the attribute to get/set, the name of the
		         Getter/Setter method.
		DETAILS: Creates a function that gets & sets (along with the DB value) an attribute.
		RETURNS: A function that gets & sets (along with the DB value) an attribute.
		"""
		db_function_name: str = db_prefix + attribute_name
		def getter_setter_method(*value: List[Any]) -> bool:
			# ———— GETTER ———— #
			if(len(value) == 0):
				return getattr(self, attribute_name);

			# ———— SETTER ———— #
			if(value[0] == getattr(self, attribute_name)):
				return True;  # values match, take the easy way out

			# Gotta update DB to match structure
			DB_function = getattr(DBFunctions, db_function_name);
			if((database_is_updated_flag := DB_function(self._id, value[0]))):
				setattr(self, attribute_name, value[0]);

			return database_is_updated_flag

		getter_setter_method.__doc__ = f"""
		SUMMARY: Getter/Setter method for the {attribute_name} attribute.
		PARAMS:  Takes the value to set if value is being set, otherwise, nothing.
		DETAILS: Determines whether method is being used as a getter or as a setter. If getter, the method returns
		         the attribute's value. If setter, then the value in the DB is attempted to be set, and if properly
		         set in DB, the value is set in the object.
		RETURNS: The value if the method is used as a Getter. Whether the value was successfully updated in the DB
		         if the method is used as a Setter.
		"""
		getter_setter_method.__name__ = method_name;
		return getter_setter_method;

	# ——————————————————————————————————————————————————— UTILITY  ——————————————————————————————————————————————————— #

	def try_call(self, function: callable, *params: list, default: Union[Any, None]=None) -> Union[Any, None]:
		try:
			return function(*params)
		except:
			return default;


	# —————————————————————————————————————————————————— CONVERSION —————————————————————————————————————————————————— #

	def __int__(self) -> int:
		return self._id;


	def __iter__(self, *additional_args: tuple) -> dict:
		attribute_names: list = [attribute.name() for attribute in self.attribute_types] + list(additional_args);

		object_dict = {};
		for object_attribute_name in attribute_names:
			value = getattr(self, object_attribute_name);
			if(isinstance(value, DBClass)):
				value = dict(value);
			elif(isinstance(value, list)):
				value = [dict(val) if(isinstance(val, DBClass)) else val for val in value];

			attribute_key = object_attribute_name[1:] if(object_attribute_name[0] == "_") else object_attribute_name;
			object_dict[attribute_key] = value;

		yield from object_dict.items();


	def __repr__(self) -> str:
		return str(self);


	def __str__(self) -> str:
		return dumps(dict(self), default=str);


	def __call__(self, attribute_name: str, conversion_type: Type=AttributeType):
		raise Exception("Hello exception");


	@staticmethod
	def _exclusive_match(haystack: list, **kwargs: dict) -> Any:
		try:
			for item in haystack:
				if(all(getattr(item, f"_{key}") == value for key, value in kwargs.items())):
					return item;
		except Exception as error:
			pass;

		return None;


	# Check key value types of dictonary for attributes to be passed to dictionary.
	def validate(self, attribute_types: Union[List[AttributeType], None]=None) -> None:
		if(attribute_types is None):
			attribute_types = self.attribute_types;

		for attribute_type in attribute_types:
			if(attribute_type.is_not_valid()):
				raise TypeError(str(attribute_type));
