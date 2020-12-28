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

from DB.DBFunctions import ALL_Curtain_info, Curtains as DBCurtains;
from Class.Curtains import Curtains;


class Header:
	def __init__(self, cursor : object, selected_curtain : int=1, *, error : str="", success : str="") -> None:
		self._curtains = [Curtains(*ALL_Curtain_info(cursor, int(curtain["id"]))) for curtain in DBCurtains(cursor)];
		self._error = error;
		self._success = success;
		self._selected_curtain = self._curtains[0];
		for x in range(len(self._curtains)):
			if(self._curtains[x].id() == selected_curtain): self._selected_curtain = self._curtains[x];


	def curtains(self):
		return self._curtains;


	def error(self):
		return self._error;


	def success(self):
		return self._success;


	def selected_curtain(self, curtain_id : int=None) -> Union[int, None]:
		if(isinstance(curtain_id, type(None))): return self._selected_curtain;
		self._selected_curtain = curtain_id;
