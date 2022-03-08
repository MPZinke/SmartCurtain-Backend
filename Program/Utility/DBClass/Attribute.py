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


class Attribute:
	def __init__(self, name: Union[str, object]):
		self._name: str = name;


	def __eq__(self, AttrType_or_Value) -> bool:
		from Utility.DBClass.AttributeType import AttributeType;
		from Utility.DBClass.AttributeValue import AttributeValue;

		if(not isinstance(AttrType_or_Value, AttributeType) and not isinstance(AttrType_or_Value, AttributeValue)):
			raise Exception(f"'{type(AttrType_or_Value)}' is not of type AttributeType or AttributeValue");

		if(self._name != AttrType_or_Value.name()):
			return False;

		if(isinstance(AttrType_or_Value, AttributeValue)):
			return type(AttrType_or_Value.value()) in self._types;

		# Compare AttributeTypes
		attr_types = AttrType_or_Value.types();
		return any(attr1_type == attr2_type for attr1_type in self._types for attr2_type in attr_types);


	def __ne__(self, AttrType_or_Value) -> bool:
		return not (self == AttrType_or_Value);


	def name(self) -> str:
		return self._name;
