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
from typing import Union;

from Other.Class.DBClass import DBClass;


class CurtainOption(DBClass):
	def __init__(self, **curtain_option):
		DBClass.__init__(self, "UPDATE_CurtainsOption", **curtain_option);

		self._data = self.try_call(json.loads, self._data, default="");


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;


	def name(self) -> str:
		return self._name;
