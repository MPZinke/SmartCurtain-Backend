#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.10.14                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import json
from paho.mqtt.client import Client as MQTTClient
from typing import Optional


from SmartCurtain.Option import Option
from SmartCurtain.AreaEvent import AreaEvent
from SmartCurtain.AreaOption import AreaOption
from SmartCurtain.Curtain import Curtain
from SmartCurtain.Room import Room
from SmartCurtain.Home import Home
from Utility.ZThread import ZWidget


class SmartCurtain(MQTTClient, ZWidget):
	def __init__(self):
		MQTTClient.__init__(self)
		ZWidget.__init__(self, "SmartCurtain", self)
		self._Homes: list[Home] = []
		self._Options: list[Option] = []


	def __iter__(self) -> dict:
		yield from {
			"Curtains": [dict(curtain) for curtain in self._Curtains],
			"Options": [dict(option) for option in self._Options]
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str)


	def _loop_process(self) -> None:
		self.connect("localhost", 1883, 60)
		self.loop_forever()


	# ————————————————————————————————————————————————————— MQTT ————————————————————————————————————————————————————— #

	def on_connect(self, client, userdata, flags, result_code) -> None:
		print(f"Connected with result code {str(result_code)}")
		self.subscribe("SmartCurtain")
		self.publish("SmartCurtain/all", """{"type": "status"}""")


	def on_message(self, client, userdata, message) -> None:
		curtain_info: dict = json.loads(message.payload)
		print(curtain_info)


	# ——————————————————————————————————————————————— GETTERS/SETTERS  ——————————————————————————————————————————————— #

	def __getitem__(self, Home_id: int) -> Optional[Home]:
		return next((home for home in self._Homes if(home.id() == Home_id)), None)


	def Room(self, Room_id: int) -> Optional[Room]:
		for home in self._Homes:
			if((room := home[Room_id]) is not None):
				return room

		return None


	def Curtain(self, Curtain_id: int) -> Optional[Curtain]:
		for home in self._Homes:
			for room in home.Rooms():
				if((curtain := room[Curtain_id]) is not None):
					return curtain

		return None
