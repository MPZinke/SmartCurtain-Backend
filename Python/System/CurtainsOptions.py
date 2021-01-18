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

from System.CurtainsOptionsKeyValues import CurtainsOptionsKeyValues;
from DB.DBCredentials import *;
from DB.DBFunctions import __CONNECT__, __CLOSE__, current_CurtainsOptionsKeyValues_for_CurtainsOptions_id as CurtOptKV;


class CurtainsOptions:
	def __init__(self, curtains_options : dict):
		self._id : int = curtains_options["id"];
		self._Curtains_id : int = curtains_options["Curtains.id"];
		self._Options_id : int = curtains_options["Options.id"];
		self._is_on : bool = bool(curtains_options["is_on"]);
		self._notes : str = curtains_options["notes"];

		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		self._CurtainsOptionsKeyValues = [CurtainsOptionsKeyValues(kv) for kv in CurtOptKV(cursor, self._id)];
		__CLOSE__(cnx, cursor);


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;


	def Curtains_id(self) -> int:
		return self._Curtains_id;


	def Options_id(self) -> int:
		return self._Options_id;


	# Helper function for managing what happens to DB data & attributes.
	# Take the name of the attribute that is affected & that setting value (if being set).
	# Sets a new value if a new value is passed.
	# Will return the original value if no new value is passed. Returns whether new value successfully set.
	def _get_or_set_attribute(self, attribute_name : str, new_value=None):
		if(isinstance(new_value, type(None))): return getattr(self, attribute_name);

		if(new_value == getattr(self, attribute_name)): return True;  # values match, take the easy way out
		# gotta update DB to match structure
		import DB.DBFunctions as DBFunctions;
		DB_function = getattr(DBFunctions, "set_CurtainsOption"+attribute_name);
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		success_flag = DB_function(cnx, cursor, self._id, new_value);
		if(success_flag): setattr(self, attribute_name, new_value);
		return success_flag + bool(__CLOSE__(cnx, cursor));


	def is_on(self, new_is_on : bool=None):
		return self._get_or_set_attribute("_is_on", new_is_on);


	def notes(self, new_notes : str=None):
		return self._get_or_set_attribute("_notes", new_notes);


	def CurtainsOptionsKeyValues(self) -> list:
		return [CurtOptKV for CurtOptKV in self._CurtainsOptionsKeyValues];


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self):
		attrs = ["_id", "_Curtains_id", "_Options_id", "_is_on", "_notes"];
		class_dict = {attr : getattr(self, attr) for attr in attrs};
		class_dict["_CurtainsOptionsKeyValues"] = {kv : self._CurtainsOptionsKeyValues[kv].dict() \
		  for kv in self._CurtainsOptionsKeyValues};


	def print(self, tab=0, next_tab=0):
		attrs = ["_id", "_Curtains_id", "_Options_id", "_is_on", "_notes"];
		for attr in attrs: print('\t'*tab, attr, " : ", getattr(self, attr));
		print('\t'*tab, "_CurtainsOptionsKeyValues : ");
		for kv in self._CurtainsOptionsKeyValues: self._CurtainsOptionsKeyValues[kv].print(tab+next_tab, next_tab);
