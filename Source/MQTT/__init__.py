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


import json
import os
from paho.mqtt.client import Client
import threading


from SmartCurtain import SmartCurtain


assert(MQTT_HOST := os.getenv("SMARTCURTAIN_MQTT_HOST")), "'SMARTCURTAIN_MQTT_HOST' cannot evaluate to False"


class MQTTClient(Client):
	def __init__(self, smart_curtain: SmartCurtain):
		Client.__init__(self)
		self._thread = threading.Thread(name="MQTTClient", target=self)

		self._SmartCurtain = smart_curtain


	def __call__(self) -> None:
		self.connect(MQTT_HOST, 1883, 60)
		self.loop_forever()


	def start(self) -> None:
		self._thread.start()


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str)


	# ————————————————————————————————————————————————————— MQTT ————————————————————————————————————————————————————— #

	def on_connect(self, client, userdata, flags, result_code) -> None:
		print(f"Connected with result code {str(result_code)}")
		self.subscribe("SmartCurtain/hub/error")
		self.subscribe("SmartCurtain/hub/update")
		self.publish("SmartCurtain/all/status", "")


	def on_message(self, client, userdata, message) -> None:
		# Status: The request for something's (a curtain's) status
		# Updates: Specify the data to update.
		# HUB ——status--> Curtain ——update--> Hub [——update--> Curtain]
		#	IE. Hub: "What is your status?", Curtain: "Let me update you"[, Hub: "Let me tweak that"]
		# Curtain ——update--> Hub [——update--> Curtain]
		#	IE. Curtain: "This is what you should show for me"[, Hub: "Let me tweak that"]
		# The Hub can however override on home, room, length, and other DB defined values.
		# However, the Hub will not override is_moving or percentage
		try:
			print(type := message.topic.split("/")[-1], end=": ")
			print(request := json.loads(message.payload))

			if(type == "error"):
				print(f"Error received: {message.payload}")

			elif(type == "update"):
				curtain = self._SmartCurtain["-"]["-"][request["id"]]

				# Values that are updated by curtain
				if(request["is_moving"] != curtain.is_moving()):
					curtain.is_moving(request["is_moving"])
				if(request["percentage"] != curtain.percentage):
					curtain.percentage(request["percentage"])

				# Values for Curtain that can be updated
				curtain_info = curtain.structure()
				if(curtain.length is not None):
					curtain_info["length"] = curtain.length
				# Movement overriding values
				if((option := curtain.CurtainOption("Auto Correct")) is not None):
					curtain_info["Auto Correct"] = option.is_on()

				if(any(curtain_info[key] != request[key] for key in ["Home.id", "Room.id", "Auto Correct"])
				  or ("length" in curtain_info and curtain_info["length"] < request["length"])):
					self.publish(f"""SmartCurtain/-/-/{request["id"]}/update""", json.dumps(curtain_info))

		except Exception as error:
			print(error)
