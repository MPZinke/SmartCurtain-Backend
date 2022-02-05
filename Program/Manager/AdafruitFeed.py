#!/usr/bin/env python3
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
from datetime import datetime, timedelta;
from os import getenv as os_getenv;
import ssl;
from time import sleep;
import warnings;
from warnings import warn as Warn;

from Manager.ManagerGlobal import *;
from Other.Class.ZWidget import ZWidget;
from Other.Global import *;
from Other.Global import try_convert, warning_message;
import Other.Logger as Logger;



class AdafruitFeed(ZWidget):
	def __init__(self, System):
		ZWidget.__init__(self, "AdafruitIO", System);

		self._option_id = self._System.Option_by_name("Adafruit Feed").id();

		warnings.formatwarning = warning_message;


	def _curtain_for_feed_id(self, feed_id):
		curtains = self._System.Curtains_list();
		for curtain in curtains:
			if(curtain.CurtainOptionKeyValue(key=feed_id)):
				return curtain;

		return None;


	# ————————————————————————————————————————————————————— MQTT ————————————————————————————————————————————————————— #

	def _activate(self, client, feed_id, position_payload):
		print(f"AdafruitFeed: client: {client}, feed_id: {feed_id}, position: {position_payload}");
		try:
			# Get the curtain for feed ID
			curtain = self._curtain_for_feed_id(feed_id);
			if(not curtain): raise Exception(f"Feed ID: {feed_id} not found");

			# Convert Option to position
			curtain_option = curtain.CurtainOption(self._option_id);
			position = try_convert(position_payload, int) or try_convert(curtain_option.data().get(feed_id, 0), int);
			print(f"Curtain: {curtain.name()}, feed: {feed_id}, position: {position}");
			if(isinstance(position, NONETYPE)): raise Exception("Could not get a valid position");

			# For selected curtain add event for position
			curtain.open_percentage(desired_position=position, Options_id=self._option_id);

		except Exception as error:
			Logger.log_error(error);


	def _connect(self, client):
		for curtain in self._System.Curtains_list():
			curtain_option = curtain.CurtainOption(self._option_id);
			# if curtain has active CurtainOption for AdafruitIO && CurtainOption has 2 CurtainOptionKeyValue:
			if(not curtain_option or not curtain_option.is_on()): continue;
			#HARDCODED: then minimum number of feeds per curtain
			current_key_values = [option for option in curtain_option.CurtainOptionKeyValues() if option.is_current()];
			if(len(current_key_values) < 2): continue;

			[client.subscribe(option.key()) for option in current_key_values];


	def _disconnect(self):
		raise Exception("MQTTClient disconnected")


	def _null(self, *args) -> None:
		return;


	def _loop_process(self):
		username = os_getenv("ADAFRUIT_IO_USERNAME");
		key = os_getenv("ADAFRUIT_IO_KEY");
		print(f"AdafruitFeed::_loop_process::username, key: {username}, {key}");
		assert(username);
		assert(key);

		ssl.SSLContext.verify_mode = ssl.VerifyMode.CERT_OPTIONAL

		client = MQTTClient(username, key, secure=False);

		client.on_connect = self._connect;
		client.on_disconnect = self._disconnect;
		client.on_message = self._activate;
		client.on_subscribe  = self._null;
		
		print("Adafruit::_loop_process");

		client.connect();
		client.loop_blocking();
