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


from datetime import datetime, timedelta;
from json import dumps as json_dumps;  # use as to be specific, but do not import too much from json
from threading import Lock;

from Class.ZWidget import ZWidget;
from DB.DBCredentials import *;
from DB.DBFunctions import __CLOSE__, __CONNECT__, Curtains as DBCurtains, Options as DBOptions;
from Other.Global import *;
from Other.Global import tomorrow_00_00;
from System.Curtains import Curtains;
from System.Options import Options;


class System(ZWidget):
	def __init__(self):
		ZWidget.__init__(self, "System", self);
		self._mutex = Lock();
		self._Curtains = None;
		self._Options = None;
		self._Options_names = None;
		self.refresh();


	def refresh(self) -> None:
		from DB.DBFunctions import Curtains as DBCurtains, Options as DBOptions;
		from DB.DBFunctions import set_all_previous_CurtainsEvent_as_activated;

		self._mutex.acquire();  # just to ensure things are executed properly
		try:
			cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);

			print("{} old events cleared".format(set_all_previous_CurtainsEvent_as_activated(cnx, cursor)));
			self._Curtains = {curtain["id"] : Curtains(curtain, self) for curtain in DBCurtains(cursor)};
			self._Options = {option["id"] : Options(option) for option in DBOptions(cursor)};
			self._Options_names = {self._Options[opt].name() : self._Options[opt].id() for opt in self._Options};

			__CLOSE__(cnx, cursor);
		finally: self._mutex.release();


	# Compliments of https://jacobbridges.github.io/post/how-many-seconds-until-midnight/
	def sleep_time(self) -> int:
		return (tomorrow_00_00() - datetime.now()).seconds + 30;  # give time to let event creators to do their thing


	def _loop_process(self) -> None:
		self.refresh();


	# ———————————————————————————————————————————————————— GETTERS ————————————————————————————————————————————————————

	def Curtain(self, Curtains_id : int):
		return self._Curtains.get(Curtains_id);


	def Curtains(self) -> dict:
		return self._Curtains;


	def Event_Curtain(self, CurtainsEvent_id : int):
		for curtain in self._Curtains:
			if(self._Curtains[curtain].CurtainsEvent(CurtainsEvent_id)): return self._Curtains[curtain];
		return None;


	def Option(self, Options_id : int):
		return self._Options.get(Options_id);


	def Option_name(self, Options_name : str):
		return self._Options_names.get(Options_name);


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
