#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on ..                                                                                                              #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


# from Class.ZWidget import ZWidget;


class Manager(ZWidget):
	def __init__(self, System):
		ZWidget.__init__(self, "Manager", 60);

		self._System = System;

		self._AdafruitFeed = AdafruitFeed(self);
		self._DaytimeEvents = DaytimeEvents(self);
		self._EventPredictor = EventPredictor(self);
		self._SunriseEvents = SunriseEvents(self);
		self._SunsetEvents = SunsetEvents(self);

		self._widget_list =	[
								self._AdafruitFeed, self._DaytimeEvents, self._EventPredictor,
								self._SunriseEvents, self._SunsetEvents
							];
		for wigdet in self._widget_list: widget.start();


	def _loop_process(self):
		if(not self._AdafruitFeed.is_alive()): self._AdafruitFeed = AdafruitFeed(self);
		if(not self._DaytimeEvents.is_alive()): self._DaytimeEvents = DaytimeEvents(self);
		if(not self._EventPredictor.is_alive()): self._EventPredictor = EventPredictor(self);
		if(not self._SunriseEvents.is_alive()): self._SunriseEvents = SunriseEvents(self);
		if(not self._SunsetEvents.is_alive()): self._SunsetEvents = SunsetEvents(self);


	def System(self):
		return self._System;