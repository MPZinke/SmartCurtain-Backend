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


from Global import NONETYPE;
from System.DB import AttributeType;
from System.DB import DBClass;
from Utility import Logger;


class CurtainOption(DBClass):

	ATTRIBUTE_TYPES =	[
							AttributeType("_id", int),
							AttributeType("_name", str),
							AttributeType("_data", (str, int, NONETYPE)),
							AttributeType("_Curtains_id", int),
							AttributeType("_Options_id", int),
							AttributeType("_is_on", (bool, int)),
							AttributeType("_notes", (int, str, NONETYPE))
						];

	def __init__(self, **curtain_option):
		DBClass.__init__(self, "UPDATE_CurtainsOption", **curtain_option);
		self.validate();

		try:
			if(self._data is not None):
				self._data = json.loads(self._data if(isinstance(self._data, str)) else str(self._data));

		except Exception as error:
			print(type(self._data));
			Logger.log_error(error);


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str);


	def __repr__(self) -> str:
		return str(self);


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;


	def name(self) -> str:
		return self._name;
