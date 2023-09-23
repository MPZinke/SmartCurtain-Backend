#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.09.23                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from Adafruit_IO import MQTTClient;
from os import getenv as os_getenv;
import ssl;
import warnings;


from Global import *;
from SmartCurtain import SmartCurtain;
from Utility import try_convert, warning_message;
from Utility import Logger;
from Utility.ZThread import ZWidget;



class AdafruitFeed(ZWidget):
	def __init__(self, smart_curtain: SmartCurtain):
		ZWidget.__init__(self, "AdafruitIO", smart_curtain);

		self._option_id = self._SmartCurtain.Option(name="Adafruit Feed").id();

		warnings.formatwarning = warning_message;


	def _curtain_for_feed_id(self, feed_id):
		"""
		SUMMARY: Determines the curtain based on the feed_id.
		"""
		curtains = self._SmartCurtain.Curtains();
		for curtain in curtains:
			if(feed_id in curtain.CurtainOptions(Options_id=self._option_id).data()):
				return curtain;

		return None;


	# ————————————————————————————————————————————————————— MQTT ————————————————————————————————————————————————————— #

	def _activate(self, client, feed_id, percentage_payload):
		try:
			# Get the curtain for feed ID
			curtain = self._curtain_for_feed_id(feed_id);
			if(not curtain):
				raise Exception(f"Feed ID: {feed_id} not found");

			# Convert Option to percentage
			curtain_option = curtain.CurtainOption(Option_id=self._option_id);
			percentage = try_convert(percentage_payload, int) or try_convert(curtain_option.data().get(feed_id,0), int);
			print(f"Curtain: {curtain.name()}, feed: {feed_id}, percentage: {percentage}");
			if(percentage is None):
				raise Exception("Could not get a valid percentage");

			# For selected curtain add event for percentage
			curtain.open(percentage, Options_id=self._option_id);

		except Exception as error:
			Logger.log_error(error);


	def _connect(self, client):
		for curtain in self._SmartCurtain.Curtains():
			curtain_option = curtain.CurtainOption(id=self._option_id);
			# if curtain has active CurtainOption for AdafruitIO && CurtainOption has 2 CurtainOptionKeyValue:
			if(not curtain_option or not curtain_option.is_on()):
				continue;

			#HARDCODED: the minimum number of feeds per curtain
			if(len(curtain_option.data()) < 2):
				continue;

			[client.subscribe(option) for option in curtain_option.data()];


	def _disconnect(self):
		raise Exception("MQTTClient disconnected")


	def _null(self, *_: list) -> None:
		return;


	def _loop_process(self):
		username = os_getenv("ADAFRUIT_IO_USERNAME");
		key = os_getenv("ADAFRUIT_IO_KEY");
		assert(username and key);

		ssl.SSLContext.verify_mode = ssl.VerifyMode.CERT_OPTIONAL

		client = MQTTClient(username, key, secure=False);

		client.on_connect = self._connect;
		client.on_disconnect = self._disconnect;
		client.on_message = self._activate;
		client.on_subscribe  = self._null;

		client.connect();
		client.loop_blocking();
