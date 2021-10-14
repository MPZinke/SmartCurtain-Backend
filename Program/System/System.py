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

from Other.Class.ZWidget import ZWidget;
from Other.DB.DBCredentials import *;
from Other.DB.DBFunctions import __CLOSE__, __CONNECT__;
from Other.DB.DBFunctions import SELECT_Curtains, SELECT_Options, UPDATE_all_prior_CurtainsEvents_is_activated;
from Other.Global import *;
from Other.Global import tomorrow_00_00;
from System.Curtain import Curtain;
from System.Option import Option;


class System(ZWidget):
	def __init__(self):
		ZWidget.__init__(self, "System", self);
		self._mutex = Lock();
		self._Curtains = None;
		self._Options = None;
		self._Options_names = None;
		self.refresh();


	def refresh(self) -> None:
		self._mutex.acquire();  # just to ensure things are executed properly
		try:
			cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);

			print(f"{UPDATE_all_prior_CurtainsEvents_is_activated(cnx, cursor)} old events cleared");  #TESTING
			selected_curtains = SELECT_Curtains(cursor);
			self._Curtains = {curtain["id"]: Curtain(**{**curtain, "System": self}) for curtain in selected_curtains};
			self._Options = {option["id"]: Option(**option) for option in SELECT_Options(cursor)};
			self._Options_names = {self._Options[opt].name(): self._Options[opt] for opt in self._Options};

			__CLOSE__(cnx, cursor);
		finally: self._mutex.release();


	# Compliments of https://jacobbridges.github.io/post/how-many-seconds-until-midnight/
	def sleep_time(self) -> int:
		return (tomorrow_00_00() - datetime.now()).seconds + 30;  # give time to let event creators to do their thing


	def _loop_process(self) -> None:
		self.refresh();


	# ———————————————————————————————————————————————————— GETTERS ————————————————————————————————————————————————————

	def Curtain(self, Curtain_id: int):
		return self._Curtains.get(Curtain_id);


	def Curtains(self) -> dict:
		return self._Curtains;


	def Event_Curtain(self, CurtainEvent_id: int):
		for curtain in self._Curtains:
			if(self._Curtains[curtain].CurtainEvent(CurtainEvent_id)):
				return self._Curtains[curtain];
		return None;


	def Option(self, Options_id: int):
		return self._Options.get(Options_id);


	# Get an Option by its name.
	def Option_name(self, Options_name: str):
		return self._Options_names.get(Options_name);


	def Options(self) -> dict:
		return self._Options;


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self):
		class_dict = {};
		class_dict["_Curtains"] = {curtain: self._Curtains[curtain].dict() for curtain in self._Curtains};
		class_dict["_Options"] = {option: self._Options[option].dict() for option in self._Options};
		return class_dict;


	def print(self, tab=0, next_tab=0):
		print('\t'*tab, "_Curtains: ");
		for curtain in self._Curtains: self._Curtains[curtain].print(tab+next_tab, next_tab);
		print('\t'*tab, "_Options: ");
		for option in self._Options: self._Options[option].print(tab+next_tab, next_tab);
