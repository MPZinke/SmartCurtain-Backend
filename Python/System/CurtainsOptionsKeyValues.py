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


	def is_current(self, new_is_current : Union[bool, None]=None) -> Union[bool, None]:
		if(isinstance(new_is_current, type(None))): return self._is_current;
		self._is_current = new_is_current;


	def key(self, new_key : Union[str, None]=None) -> Union[str, None]:
		if(isinstance(new_key, type(None))): return self._key;
		self._key = new_key;


	def value(self, new_value : Union[str, None]=None) -> Union[str, None]:
		if(isinstance(new_value, type(None))): return self._value;
		self._value = new_value;


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self):
		attrs = ["_id", "_CurtainsOptions_id", "_is_current", "_key", "_value"];
		return {attr : getattr(self, attr) for attr in attrs};


	def print(self, tab=0, next_tab=0):
		attrs = ["_id", "_CurtainsOptions_id", "_is_current", "_key", "_value"];
		for attr in attrs: print('\t'*tab, attr, " : ", getattr(self, attr));
