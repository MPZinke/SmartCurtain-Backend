#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.10.14                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from Utility import Generic


from datetime import datetime, timedelta
from typing import Any


def midnight() -> datetime:
	"""
	SUMMARY: Get the datetime object for the next day at 00:00:00.
	NOTES:   Compliments of https://jacobbridges.github.io/post/how-many-seconds-until-midnight/
	"""
	tomorrow = datetime.now() + timedelta(1)
	return datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=0, minute=0, second=0)


def substr(string: str, *span: list) -> str:
	"""
	SUMMARY: Gets the substring from a string using a list parameter.
	PARAMS:  Takes the string to get substring from, list of start and end points.
	NOTES:   Sugar. Uses standard substring method
	"""
	if(len(span) == 0):
		return string
	if(len(span) == 1):
		return string[:span[0]]

	return string[span[0]: span[1]]


def temp(attributes: dict, *, base_class=(), name: str="Temp") -> object:
	"""
	SUMMARY: Creates a temporary object with the given attributes, base_class, and name.
	PARAMS:  Takes the attributes to add to the temp object, the name of the object.
	RETURNS: A temporary object with the given attributes, base_class, and name.
	"""
	return type(name, base_class, attributes)()


def time_to_midnight(start_time: object=None) -> int:
	"""
	SUMMARY: Determines the time until tomorrow.
	PARAMS:  Takes the time to calculate from or defaults to now.
	RETURNS: The number of seconds until midnight.
	"""
	if(start_time is None):
		start_time = datetime.now()

	return (midnight() - start_time).seconds


def try_convert(value, value_type, default=None) -> Any:
	"""
	SUGAR: tries to convert a value to the specified type.
	Takes value to convert, type to convert to.
	If it fails, returns None.
	"""
	try:
		return value_type(value)
	except:
		return default


def warning_message(message, *_: list) -> str:
	"""
	SUMMARY: Used to override warning format & return only the warning message.
	"""
	return str(message)+"\n"
