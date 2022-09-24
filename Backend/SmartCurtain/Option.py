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


from SmartCurtain.DB import AttributeType, DBClass;


class Option(DBClass):
	ATTRIBUTE_TYPES =	[
							AttributeType("_id", int),
							AttributeType("_name", str),
							AttributeType("_description", str),
							AttributeType("_is_current", int)
						];


	def __init__(self, **option_info):
		DBClass.__init__(self, "UPDATE_Option", **option_info);

		self.validate();


	# ———————————————————————————————————————————————— GETTERS/SETTERS ————————————————————————————————————————————————

	def id(self) -> int:
		return self._id;
