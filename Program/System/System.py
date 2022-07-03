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
from json import dumps;
from socket import gethostbyname, gethostname;
from threading import Lock;
from typing import Any, List, Union;


from Global import *;
from System.Curtain import Curtain;
from System.Option import Option;
from Utility import tomorrow_00_00;
from Utility.DB import SELECT_Curtains, SELECT_Options;
from Utility.DB import DBClass;
from Utility.ZThread import ZWidget;


class System(ZWidget):
	def __init__(self):
		ZWidget.__init__(self, "System", self);
		self._mutex = Lock();
		self._Curtains: List[Curtain] = [];
		self._Options: List[Option] = [];

		self._IP_Address = gethostbyname(gethostname());

		self.refresh();


	# SUMMARY: Used for if DB values have changed and System information needs to be refreshed.
	def refresh(self) -> None:
		import inspect;
		self._mutex.acquire();  # just to ensure things are executed properly
		try:
			selected_curtains = SELECT_Curtains();
			# Cleanup events since destructor doesn't work, especially when called by dict reassignment.
			[curtain.delete_events() for curtain in self._Curtains];
			self._Curtains = [Curtain(**{**curtain, "System": self}) for curtain in selected_curtains];
			self._Options = [Option(**option) for option in SELECT_Options()];
			dicts = [dict(curtain) for curtain in self._Curtains];
			print(dicts);

		finally:
			self._mutex.release();


	# Compliments of https://jacobbridges.github.io/post/how-many-seconds-until-midnight/
	def sleep_time(self) -> int:
		return (tomorrow_00_00() - datetime.now()).seconds + 30;  # give time to let event creators to do their thing


	def _loop_process(self) -> None:
		self.refresh();


	# ———————————————————————————————————————————————————— GETTERS ————————————————————————————————————————————————————

	@staticmethod
	def _exclusive_match(haystack: list, **kwargs: dict) -> Any:
		try:
			for item in haystack:
				if(all(getattr(item, f"_{key}") == value for key, value in kwargs.items())):
					return item;
		except Exception as error:
			pass;

		return None;


	def Curtain(self, **kwargs: dict) -> Union[Curtain, None]:
		return System._exclusive_match(self._Curtains, **kwargs);


	def Curtains(self) -> List[Curtain]:
		return self._Curtains;


	def Option(self, **kwargs: dict) -> Union[Option, None]:
		return System._exclusive_match(self._Options, **kwargs)


	def Options(self) -> dict:
		return self._Options;


	def IP_Address(self) -> str:
		return self._IP_Address;


	# ———————————————————————————————————————————————————— UTILITY ————————————————————————————————————————————————————

	def dict(self):
		class_dict = {};
		class_dict["_Curtains"] = {curtain: self._Curtains[curtain].dict() for curtain in self._Curtains};
		class_dict["_Options"] = {option: self._Options[option].dict() for option in self._Options};
		return class_dict;


	def print(self, tab=0, next_tab=0):
		print('\t'*tab, "_Curtains: ");
		for curtain in self._Curtains:
			self._Curtains[curtain].print(tab+next_tab, next_tab);
		print('\t'*tab, "_Options: ");
		for option in self._Options:
			self._Options[option].print(tab+next_tab, next_tab);
