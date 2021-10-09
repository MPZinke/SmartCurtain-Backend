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

from Class.DBClass import DBClass;
from DB.DBCredentials import *;
from DB.DBFunctions import __CONNECT__, __CLOSE__, SELECT_current_CurtainsOptionsKeyValues_for_CurtainsOptions_id;
from System.CurtainOptionKeyValue import CurtainOptionKeyValue;


class CurtainOption(DBClass):
	def __init__(self, **curtain_option):
		DBClass.__init__(self, "UPDATE_CurtainsOption", **curtain_option);

		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		option_key_values = SELECT_current_CurtainsOptionsKeyValues_for_CurtainsOptions_id(cursor, self._id);
		self._CurtainOptionKeyValues = [CurtainOptionKeyValue(**kv) for kv in option_key_values];
		__CLOSE__(cnx, cursor);


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;


	def name(self) -> str:
		return self._name;


	def CurtainOptionKeyValues(self) -> list:
		return [CurtOptKV for CurtOptKV in self._CurtainOptionKeyValues];


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self):
		attrs = ["_id", "_Curtains_id", "_Options_id", "_is_on", "_notes"];
		class_dict = {attr : getattr(self, attr) for attr in attrs};
		class_dict["CurtainOptionKeyValues"] = {kv : self._CurtainOptionKeyValues[kv].dict() \
		  for kv in self._CurtainOptionKeyValues};


	def print(self, tab=0, next_tab=0):
		attrs = ["_id", "_Curtains_id", "_Options_id", "_is_on", "_notes"];
		for attr in attrs: print('\t'*tab, attr, " : ", getattr(self, attr));
		print('\t'*tab, "CurtainOptionKeyValues : ");
		for kv in self._CurtainOptionKeyValues: self._CurtainOptionKeyValues[kv].print(tab+next_tab, next_tab);
