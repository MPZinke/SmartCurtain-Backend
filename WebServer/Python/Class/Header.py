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


from typing import Union;


from Python.DB.DBFunctions import ALL_Curtain_info, Curtains as DBCurtains;
from Python.Class.Curtains import Curtains;


class Header:
	def __init__(self, cursor):
		self._curtains = [Curtains(*ALL_Curtain_info(cursor, curtain["id"])) for curtain in DBCurtains(cursor)];
		self._selected_curtain = 0;


	def curtains(self):
		return self._curtains;


	def selected_curtain(self, curtain_id : int=None):
		if(isinstance(curtain_id, type(None))): return self._selected_curtain;
		self._selected_curtain = curtain_id;
