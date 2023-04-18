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
		self.subscribe("SmartCurtain/hub/update")
		self.publish("SmartCurtain/all/status", "")


	def on_message(self, client, userdata, message) -> None:
		try:
			node_dict: dict = json.loads(message.payload)
		except:
			node_dict = {"id": 0}

		print(node_dict)
		if((curtain := self.Curtain(node_dict.get("id"))) is None):
			return  # ignore invalid calls

		curtain.is_connected(True)
		if("is_moving" in node_dict):
			curtain.is_moving(node_dict["is_moving"])
		if("Auto Calibrate" in node_dict and "length" in node_dict and curtain.CurtainOption("Auto Calibrate").is_on()):
			curtain.length(node_dict["length"])
		if("percentage" in node_dict):
			curtain.percentage(node_dict["percentage"])

		curtain_dict = curtain.node_dict()
		if(any((key in curtain_dict and curtain_dict[key] != node_dict[key]) for key in node_dict)):
			print("Values do not match")
			self.publish(f"""SmartCurtain/-/-/{curtain.id()}/update""", json.dumps(curtain_dict))


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
