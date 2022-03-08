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


from typing import Any, Union;


from Utility.DBClass.Attribute import Attribute;


class AttributeType(Attribute):
	def __init__(self, name: Union[str, object], types: Union[Any, list]):
		Attribute.__init__(self, name);
		self._types: Union[Any, list] = types if(isinstance(types, list)) else [types];


	def types(self) -> str:
		return self._types;


	def allowed_types(self) -> str:
		return " or ".join([type_instance.__name__ for type_instance in self._types]);
