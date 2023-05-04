#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2023.05.04                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from paho.mqtt.client import Client
import threading


from SmartCurtain import SmartCurtain


class MQTTClient(Client):
	def __init__(self, smart_curtain: SmartCurtain):
		Client.__init__(self)
		self._thread = threading.Thread(name="MQTTClient", target=self)

		self._SmartCurtain = smart_curtain


	def __call__(self) -> None:
		self.connect("localhost", 1883, 60)
		self.loop_forever()


	def start(self) -> None:
		self._thread.start()


	def __iter__(self) -> dict:
		yield from {
			"Curtains": [dict(curtain) for curtain in self._Curtains],
			"Options": [dict(option) for option in self._Options]
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str)


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
