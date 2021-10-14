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

from Other.Class.DBClass import DBClass;


class CurtainOptionKeyValue(DBClass):
	def __init__(self, **curtain_option_key_value_info):
		DBClass.__init__(self, "UPDATE_CurtainsOptionsKeyValues", **curtain_option_key_value_info);


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self):
		attrs = ["_id", "_CurtainsOptions_id", "_is_current", "_key", "_value"];
		return {attr : getattr(self, attr) for attr in attrs};


	def print(self, tab=0, next_tab=0):
		attrs = ["_id", "_CurtainsOptions_id", "_is_current", "_key", "_value"];
		for attr in attrs: print('\t'*tab, attr, " : ", getattr(self, attr));
