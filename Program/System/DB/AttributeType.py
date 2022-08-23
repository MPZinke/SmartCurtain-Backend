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


class AttributeType:
	def __init__(self, obj: object, attribute_name: str, types: Union[Any, list]):
		self._object: object = obj;
		self._attribute_name: str = attribute_name;
		self._types: Union[Any, tuple] = types;


	def __str__(self) -> str:
		attribute_name: str = self._attribute_name;
		attribute_value: Any = self.value();
		value_type_str: str = type(attribute_value.value()).__name__;
		allowed_type_str: str = " or ".join([type_instance.__name__ for type_instance in self._types]);

		if(self.is_valid()):
			return f"'{attribute_name}' value {attribute_value} is of valid type {value_type_str}";

		return f"'{attribute_name}' value {attribute_value}, type: {value_type_str} is not of type {allowed_type_str}";


	def __contains__(self, type) -> bool:
		if(isinstance(self._types, tuple)):
			return type in self._types;

		return type == self._types;


	def is_valid(self) -> bool:
		if(not hasattr(self._object, self._attribute_name)):
			raise TypeError(f"DB Object is missing attribute: {self._attribute_name}");

		value: Any = getattr(self._object, self._attribute_name);
		return isinstance(value, self._types);


	def is_not_valid(self) -> bool:
		if(not hasattr(self._object, self._attribute_name)):
			raise TypeError(f"DB Object is missing attribute: {self._attribute_name}");

		value: Any = getattr(self._object, self._attribute_name);
		return not isinstance(value, self._types);


	def name(self) -> str:
		return self._attribute_name;


	def types(self) -> str:
		return self._types;


	def value(self) -> Any:
		if(not hasattr(self._object, self._attribute_name)):
			raise TypeError(f"DB Object is missing attribute: {self._attribute_name}");

		return getattr(self._object, self._attribute_name);
