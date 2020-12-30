#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.23                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from typing import Union;


class Options:
	def __init__(self, option_info : dict):
		self._id : int = option_info["id"];
		self._description : str = option_info["description"];
		self._is_current : bool = bool(option_info["is_current"]);
		self._name : str = option_info["name"];


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self, new_id : int=None) -> Union[int, None]:
		if(isinstance(new_id, type(None))): return self._id;
		self._id = new_id;


	def description(self, new_description : str=None) -> Union[str, None]:
		if(isinstance(new_description, type(None))): return self._description;
		self._description = new_description;


	def is_current(self, new_is_current : bool=None) -> Union[bool, None]:
		if(isinstance(new_is_current, type(None))): return self._is_current;
		self._is_current = new_is_current;


	def name(self, new_name : str=None) -> Union[str, None]:
		if(isinstance(new_name, type(None))): return self._name;
		self._name = new_name;


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self):
		attrs = ["_id", "_description", "_is_current", "_name"];
		return {attr : getattr(self, attr) for attr in attrs};


	def print(self, tab=0, next_tab=0):
		attrs = ["_id", "_description", "_is_current", "_name"];
		for attr in attrs: print('\t'*tab, attr, " : ", getattr(self, attr));
