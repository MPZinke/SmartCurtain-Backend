#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.29                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from typing import Union;


class CurtainsOptionsKeyValues:
	def __init__(self, curtains_options_key_value_info : dict):
		self._id : int = curtains_options_key_value_info["id"];
		self._CurtainsOptions_id : int = curtains_options_key_value_info["CurtainsOptions.id"];
		self._is_current : bool = bool(curtains_options_key_value_info["is_current"]);
		self._key : str = curtains_options_key_value_info["key"];
		self._value : str = curtains_options_key_value_info["value"];


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;


	def CurtainsOptions_id(self) -> int:
		return self._CurtainsOptions_id;


	# Helper function for managing what happens to DB data & attributes.
	# Take the name of the attribute that is affected & that setting value (if being set).
	# Sets a new value if a new value is passed.
	# Will return the original value if no new value is passed. Returns whether new value successfully set.
	def _get_or_set_attribute(self, attribute_name : str, new_value=None):
		if(isinstance(new_value, type(None))): return getattr(self, attribute_name);

		if(new_value == getattr(self, attribute_name)): return True;  # values match, take the easy way out
		# gotta update DB to match structure
		import DB.DBFunctions as DBFunctions;
		DB_function = getattr(DBFunctions, "set_CurtainsOptionsKeyValues"+attribute_name);
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		success_flag = DB_function(cnx, cursor, self._id, new_value);
		if(success_flag): setattr(self, attribute_name, new_value);
		return success_flag + bool(__CLOSE__(cnx, cursor));


	def is_current(self, new_is_current : bool=None):
		return self._get_or_set_attribute("_is_current", new_is_current);


	def key(self, new_key : str=None):
		return self._get_or_set_attribute("_key", new_key);


	def value(self, new_value : str=None):
		return self._get_or_set_attribute("_value", new_value);


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self):
		attrs = ["_id", "_CurtainsOptions_id", "_is_current", "_key", "_value"];
		return {attr : getattr(self, attr) for attr in attrs};


	def print(self, tab=0, next_tab=0):
		attrs = ["_id", "_CurtainsOptions_id", "_is_current", "_key", "_value"];
		for attr in attrs: print('\t'*tab, attr, " : ", getattr(self, attr));
