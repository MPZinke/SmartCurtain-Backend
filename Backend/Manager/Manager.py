#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.01.17                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION: Manages the individual threads that create events based on options set by the user. Checks every 30   #
#     seconds that all subprocesses are running. If not, restarts subproprocess.                                       #
#   BUGS:       -MQTTClient::connect() can fail without recording errors, but does not crash thread                    #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from Manager import AdafruitFeed, SunriseOpen, SunsetClose;
from SmartCurtain import SmartCurtain;
from Utility.ZThread import ZWidget;


class Manager(ZWidget):
	def __init__(self, smart_curtain: SmartCurtain):
		ZWidget.__init__(self, "Manager", smart_curtain, 60);

		# self._AdafruitFeed = AdafruitFeed(self._SmartCurtain);
		# self._EventPredictor = EventPredictor(self._SmartCurtain);
		self._SunriseOpen = SunriseOpen(self._SmartCurtain);
		self._SunsetClose = SunsetClose(self._SmartCurtain);

		self._widget_list =	[
								# self._AdafruitFeed,
								# self._EventPredictor,
								self._SunriseOpen,
								self._SunsetClose
							];
		for widget in self._widget_list: widget.start();


	def _loop_process(self):
		# if(not self._AdafruitFeed.is_alive()):
		# 	self._AdafruitFeed = AdafruitFeed(self);
		# if(not self._DaytimeEvents.is_alive()):
		# 	self._DaytimeEvents = DaytimeEvents(self);
		# if(not self._EventPredictor.is_alive()):
		# 	self._EventPredictor = EventPredictor(self);
		if(not self._SunriseOpen.is_alive()):
			self._SunriseOpen = SunriseOpen(self);
		if(not self._SunsetClose.is_alive()):
			self._SunsetClose = SunsetClose(self);


	def SmartCurtain(self):
		return self._SmartCurtain;
