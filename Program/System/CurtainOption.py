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


import json;
from json import dumps;
from typing import Union;


from Global import NONETYPE;
from Utility.DBClass import AttributeType;
from Utility.DBClass import DBClass;


class CurtainOption(DBClass):
	def __init__(self, **curtain_option):
		DBClass.__init__(self, "UPDATE_CurtainsOption", **curtain_option);
		self.attribute_types: AttributeType =	[
													AttributeType("_id", int),
													AttributeType("_Curtains_id", int),
													AttributeType("_Options_id", int),
													AttributeType("_is_on", [bool, int]),
													AttributeType("_notes", [int, str, NONETYPE])
												];
		self.validate();

		self._data = self.try_call(json.loads, self._data, default="");


	def __iter__(self) -> dict:
		return DBClass.__iter__(self, "_data");


	def __str__(self) -> str:
		return dumps(dict(self), default=str);


	def __repr__(self) -> str:
		return str(self);


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;


	def name(self) -> str:
		return self._name;
