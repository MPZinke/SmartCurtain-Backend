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
from time import sleep;
import warnings;
from warnings import warn as Warn;

from Class import ZWidget;
from Manager.ManagerGlobal import *;
from Other.Global import *;
from Other.Global import warning_message;
from Other.Logger import log_error;



class AdafruitIO(ZWidget):
	def __init__(self, System):
		ZWidget.__init__(self, "AdafruitIO", System);

		warnings.formatwarning = warning_message;


	def _curtain_list(self):
		curtains = self._System.Curtains();
		return [curtains[curtain_id] for curtain_id in curtains];


	def _curtain_for_feed_id(feed_id):
		curtains = self._curtain_list();
		for curtain in curtains:
			if(curtain.CurtainOptionKeyValue(CurtainOptionKeyValue)):
				return curtain;

		return None;


	def _activate(self, client, feed_id, position_payload):
		try:
			curtain = self._curtain_for_feed_id(feed_id);
			if(not curtain): raise Exception(f"Feed ID: {feed_id} not found");

		except Exception as error:
			log_error(error);


	def _connect(self, client):
		for curtain in self._curtain_list():
			# if curtain has CurtainOption for AdafruitIO && CurtainOption for AdafruitIO has CurtainOptionKeyValue:
				# connect
			if(curtain.CurtainOption(self.))


	def _loop_process(self):
		client = MQTTClient()  #TODO: populate

		client.on_connect = self._connect;
		client.on_disconnect = self._disconnect;
		client.on_message = self._activate;
		client.on_subscribe  = self._null
		
		client.connect();
		client.loop_blocking();
