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
from DB.DBFunctions import __CONNECT__, CurtainsOptionsKeyValues_for_CurtainsOptions_id;


class CurtainsOptions:
	def __init__(self, curtains_options : dict):
		self._id : int = curtains_options["id"];
		self._Curtains_id : int = curtains_options["Curtains.id"];
		self._Options_id : int = curtains_options["Options.id"];
		self._is_on : bool = bool(curtains_options["is_on"]);
		self._notes : str = curtains_options["notes"];

		_, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		self._CurtainsOptionsKeyValues = {};
		for kv in CurtainsOptionsKeyValues_for_CurtainsOptions_id(cursor, self._id):
			self._CurtainsOptionsKeyValues[kv["CurtainsOptions.id"]] = CurtainsOptionsKeyValues(kv);
		cursor.close();


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;


	def Curtains_id(self) -> int:
		return self._Curtains_id;


	def Options_id(self) -> int:
		return self._Options_id;


	def is_current(self, new_is_current : Union[bool, None]=None) -> Union[bool, None]:
		if(isinstance(is_current, type(None))): return self._is_current;
		self._is_current = new_is_current;


	def is_on(self, new_is_on : Union[bool, None]=None) -> Union[bool, None]:
		if(isinstance(new_is_on, type(None))): return self._is_on;
		self._is_on = new_is_on;


	def notes(self, new_notes : Union[str, None]=None) -> Union[str, None]:
		if(isinstance(notes, type(None))): return self._notes;
		self._notes = new_notes;


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
