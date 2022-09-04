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

		self.refresh();


	# SUMMARY: Used for if DB values have changed and System information needs to be refreshed.
	def refresh(self) -> None:
		try:
			self._mutex.acquire();  # just to ensure things are executed properly
			selected_curtains = SELECT_Curtains();
			# Cleanup events since destructor doesn't work, especially when called by dict reassignment.
			[curtain.delete_events() for curtain in self._Curtains];
			self._Curtains = [Curtain(**{**curtain, "System": self}) for curtain in selected_curtains];
			self._Options = [Option(**option) for option in SELECT_Options()];

		except Exception as error:
			Logger.log_error(error);


	# Compliments of https://jacobbridges.github.io/post/how-many-seconds-until-midnight/
	def sleep_time(self) -> int:
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
		NetworkLookup_host = os.getenv("NETWORKLOOKUP_HOST");
		NetworkLookup_bearer_token = os.getenv("NETWORKLOOKUP_BEARERTOKEN");
		Curtain_network_name = os.getenv("SMARTCURTAIN_NETWORKNAME");

		url = f"http://{NetworkLookup_host}/api/v1.0/network/label/{Curtain_network_name}/devices/group/label/Curtain";
		response = requests.get(url, headers={"Authorization": f"Bearer {NetworkLookup_bearer_token}"});

		if(response.status_code == 200):
			try:
				for curtain_IP in [curtain["address"] for curtain in response.json()]:
					pass

			except Exception as error:
				print(error)

