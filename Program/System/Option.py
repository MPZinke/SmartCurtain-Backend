#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.23                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from System.DB import AttributeType, DBClass;


class Option(DBClass):
	def __init__(self, **option_info):
		DBClass.__init__(self, "UPDATE_Option", **option_info);
		self.attribute_types =	[
									AttributeType(self, "_id", int),
									AttributeType(self, "_name", str),
									AttributeType(self, "_description", int),
									AttributeType(self, "_is_current", int)
								];


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;
