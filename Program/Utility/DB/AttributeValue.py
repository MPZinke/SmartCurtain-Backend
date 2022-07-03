#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.03.07                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from typing import Any;


from Utility.DB.Attribute import Attribute;


class AttributeValue(Attribute):
	def __init__(self, name, value):
		Attribute.__init__(self, name);
		self._value: Any = value;


	def types(self) -> list:
		return [type(self._value)];


	def value(self) -> Any:
		return self._value;
