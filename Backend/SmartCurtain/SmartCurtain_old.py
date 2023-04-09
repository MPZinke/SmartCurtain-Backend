# #!/opt/homebrew/bin/python3
# # -*- coding: utf-8 -*-
# __author__ = "MPZinke"

# ########################################################################################################################
# #                                                                                                                      #
# #   created by: MPZinke                                                                                                #
# #   on 2020.12.29                                                                                                      #
# #                                                                                                                      #
# #   DESCRIPTION:                                                                                                       #
# #   BUGS:                                                                                                              #
# #   FUTURE:                                                                                                            #
# #                                                                                                                      #
# ########################################################################################################################


# import json;
# import os;
# from paho.mqtt.client import Client as MQTTClient;
# import requests;
# from socket import gethostbyname, gethostname;
# from threading import Lock;
# from typing import List, Union;


# from Global import *;
# from SmartCurtain import Curtain, Option;
# from SmartCurtain.DB import SELECT_Options;
# from SmartCurtain.DB import DBClass;
# from Utility import temp, time_to_midnight;
# from Utility import Logger;
# from Utility.ZThread import ZWidget;


# class SmartCurtain(ZWidget, MQTTClient):
# 	def __init__(self):
# 		ZWidget.__init__(self, "SmartCurtain", self);
# 		MQTTClient.__init__(self)

# 		self._mutex = Lock();
# 		self._Curtains: List[Curtain] = [];
# 		self._Options: List[Option] = [];

# 		self._IP_Address = gethostbyname(gethostname());

# 		self._refresh_failures = False;  # Whether failures occurred while refreshing the curtains.
# 		self.refresh();


# 	def __iter__(self) -> dict:
# 		yield from {
# 			"Curtains": [dict(curtain) for curtain in self._Curtains],
# 			"Options": [dict(option) for option in self._Options]
# 		}.items();


# 	def __str__(self) -> str:
# 		return json.dumps(dict(self), default=str);


# 	# SUMMARY: Used for if DB values have changed and SmartCurtain information needs to be refreshed.
# 	def refresh(self) -> None:
# 		with self._mutex:
# 			# Cleanup events since destructor doesn't work, especially when called by dict reassignment.
# 			self._Options = [Option(**option) for option in SELECT_Options()];
# 			# self.check_for_Curtain_updates();


# 	def _loop_process(self) -> None:
# 		self.connect("localhost", 1883, 60)
# 		self.loop_forever()


# 	# ————————————————————————————————————————————————————— MQTT ————————————————————————————————————————————————————— #

# 	def on_connect(self, client, userdata, flags, result_code) -> None:
# 		print(f"Connected with result code {str(result_code)}")
# 		self.subscribe("curtains/hub")
# 		self.publish("curtains/all", """{"type": "status"}""")


# 	def on_message(self, client, userdata, message) -> None:
# 		curtain_info: dict = json.loads(message.payload)
# 		# if((curtain := self.Curtain(id=curtain_info.get("id"))) is None):
# 		# 	self._Curtains.append()
# 		# self.curtains[curtain_info["id"]] = curtain_info
# 		print(curtain_info)


# 	# ——————————————————————————————————————————————————— GETTERS ——————————————————————————————————————————————————— #

# 	def Curtain(self, **kwargs: dict) -> Union[Curtain, None]:
# 		return DBClass._exclusive_match(self._Curtains, **kwargs);


# 	def Curtains(self) -> List[Curtain]:
# 		return self._Curtains;


# 	def Option(self, **kwargs: dict) -> Union[Option, None]:
# 		return DBClass._exclusive_match(self._Options, **kwargs)


# 	def Options(self) -> dict:
# 		return self._Options;


# 	def IP_Address(self) -> str:
# 		return self._IP_Address;


# 	# ——————————————————————————————————————————————————— UTILITY ——————————————————————————————————————————————————— #
