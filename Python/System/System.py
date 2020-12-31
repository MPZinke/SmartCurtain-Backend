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


from json import dumps as json_dumps;  # use as to be specific, but do not import too much from json
from threading import Lock;

from Class.ZWidget import ZWidget;
from DB.DBCredentials import *;
from DB.DBFunctions import __CONNECT__, Curtains as DBCurtains, Options as DBOptions;
from Other.Global import *;
from System.Curtains import Curtains;
from System.Options import Options;


class System(ZWidget):
	def __init__(self):
		ZWidget.__init__(self, "System", SYSTEM_REFRESH_WAIT);
		self._mutex = Lock();
		self._Curtains = None;
		self._Options = None;
		self.refresh();


	def refresh(self) -> None:
		self._mutex.acquire();  # just to ensure things are executed properly
		try:
			cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);

			self._Curtains = {curtain["id"] : Curtains(curtain) for curtain in DBCurtains(cursor)};
			self._Options = {option["id"] : Options(option) for option in DBOptions(cursor)};

			cursor.close();
		finally: self._mutex.release();


	def _loop_process(self) -> None:
		self.refresh();


	# ———————————————————————————————————————————————————— GETTERS ————————————————————————————————————————————————————

	def Curtain(self, Curtains_id : int):
		return self._Curtains.get(Curtains_id);


	def Curtains(self) -> dict:
		return self._Curtains;


	def Option(self, Options_id : int):
		return self._Options.get(Options_id);


	def Options(self) -> dict:
		return self._Options;


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self):
		class_dict = {};
		class_dict["_Curtains"] = {curtain : self._Curtains[curtain].dict() for curtain in self._Curtains};
		class_dict["_Options"] = {option : self._Options[option].dict() for option in self._Options};
		return class_dict;


	def print(self, tab=0, next_tab=0):
		print('\t'*tab, "_Curtains : ");
		for curtain in self._Curtains: self._Curtains[curtain].print(tab+next_tab, next_tab);
		print('\t'*tab, "_Options : ");
		for option in self._Options: self._Options[option].print(tab+next_tab, next_tab);
