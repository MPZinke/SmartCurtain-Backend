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
from System.DB import AttributeType;
from System.DB import DBClass;
from Utility import Logger;


class CurtainOption(DBClass):
	def __init__(self, **curtain_option):
		DBClass.__init__(self, "UPDATE_CurtainsOption", **curtain_option);
		self.attribute_types =	[
									AttributeType(self, "_id", int),
									AttributeType(self, "_name", str),
									AttributeType(self, "_Curtains_id", int),
									AttributeType(self, "_Options_id", int),
									AttributeType(self, "_is_on", (bool, int)),
									AttributeType(self, "_notes", (int, str, NONETYPE))
								];
		self.validate();

		try:
			if(self._data is not None):
				self._data = json.loads(self._data if(isinstance(self._data, str)) else str(self._data));
		except Exception as error:
			print(type(self._data));
			Logger.log_error(error);


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
