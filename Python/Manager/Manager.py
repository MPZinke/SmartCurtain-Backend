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
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from Class.ZWidget import ZWidget;
from Manager.SunriseOpen import SunriseOpen;


class Manager(ZWidget):
	def __init__(self, System):
		ZWidget.__init__(self, "Manager", 60);

		self._System = System;

		# self._AdafruitFeed = AdafruitFeed(self._System);
		# self._DaytimeEvents = DaytimeEvents(self._System);
		# self._EventPredictor = EventPredictor(self._System);
		self._SunriseOpen = SunriseOpen(self._System);
		# self._SunsetEvents = SunsetEvents(self._System);

		# self._widget_list =	[
		# 						self._AdafruitFeed, self._DaytimeEvents, self._EventPredictor,
		# 						self._SunriseOpen, self._SunsetEvents
		# 					];
		# for wigdet in self._widget_list: widget.start();
		self._SunriseOpen.start();


	def _loop_process(self):
		# if(not self._AdafruitFeed.is_alive()): self._AdafruitFeed = AdafruitFeed(self);
		# if(not self._DaytimeEvents.is_alive()): self._DaytimeEvents = DaytimeEvents(self);
		# if(not self._EventPredictor.is_alive()): self._EventPredictor = EventPredictor(self);
		if(not self._SunriseOpen.is_alive()): self._SunriseOpen = SunriseOpen(self);
		# if(not self._SunsetEvents.is_alive()): self._SunsetEvents = SunsetEvents(self);


	def System(self):
		return self._System;