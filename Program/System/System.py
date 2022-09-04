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
import json;
import os;
import requests;
from socket import gethostbyname, gethostname;
from threading import Lock;
from typing import Any, List, Union;


from Global import *;
from System import Curtain, Option;
from Utility import tomorrow_00_00;
from Utility import Logger;
from System.DB import SELECT_Curtains, SELECT_Options;
from System.DB import DBClass;
from Utility.ZThread import ZWidget;


class System(ZWidget):
	def __init__(self):
		ZWidget.__init__(self, "System", self);
		self._mutex = Lock();
		self._Curtains: List[Curtain] = [];
		self._Options: List[Option] = [];

		self._IP_Address = gethostbyname(gethostname());

		self._refresh_failures = False;  # Whether failures occurred while refreshing the curtains.
		self.refresh();


	# SUMMARY: Used for if DB values have changed and System information needs to be refreshed.
	def refresh(self) -> None:
		try:
			self._mutex.acquire();  # just to ensure things are executed properly

			# Cleanup events since destructor doesn't work, especially when called by dict reassignment.
			self._Options = [Option(**option) for option in SELECT_Options()];
			self.set_Curtains();

		except Exception as error:
			Logger.log_error(error);


	# Compliments of https://jacobbridges.github.io/post/how-many-seconds-until-midnight/
	def sleep_time(self) -> int:
		if(self._refresh_failures):
			return 30;

		return (tomorrow_00_00() - datetime.now()).seconds + 30;  # give time to let event creators to do their thing


	def _loop_process(self) -> None:
		self.refresh();


	# ——————————————————————————————————————————————————— GETTERS ——————————————————————————————————————————————————— #

	def Curtain(self, **kwargs: dict) -> Union[Curtain, None]:
		return DBClass._exclusive_match(self._Curtains, **kwargs);


	def Curtains(self) -> List[Curtain]:
		return self._Curtains;


	def Option(self, **kwargs: dict) -> Union[Option, None]:
		return DBClass._exclusive_match(self._Options, **kwargs)


	def Options(self) -> dict:
		return self._Options;


	def IP_Address(self) -> str:
		return self._IP_Address;


	# ——————————————————————————————————————————————————— UTILITY ——————————————————————————————————————————————————— #

	def __iter__(self) -> dict:
		yield from {
			"Curtains": [dict(curtain) for curtain in self._Curtains],
			"Options": [dict(option) for option in self._Options]
		}.items();


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str);


	def set_Curtains(self) -> None:
		"""
		SUMMARY: Gets the curtains on the network according to the NetworkLookup.
		"""
		[curtain.delete_events() for curtain in self._Curtains];  # Clean up the curtains we are going to replace

		NetworkLookup_host = os.getenv("NETWORKLOOKUP_HOST");
		NetworkLookup_bearer_token = os.getenv("NETWORKLOOKUP_BEARERTOKEN");
		Curtain_network_name = os.getenv("SMARTCURTAIN_NETWORKNAME");

		try:
			url = f"http://{NetworkLookup_host}/api/v1.0/network/label/{Curtain_network_name}/devices/group/label/Curtain";
			response = requests.get(url, headers={"Authorization": f"Bearer {NetworkLookup_bearer_token}"});
			if(response.status_code == 200):
				self._Curtains = [Curtain(self, curtain["address"], curtain["label"]) for curtain in response.json()];

			self._refresh_failures = response.status_code != 200;

		except Exception as error:
			self._refresh_failures = True;
			Logger.log_error(error);
