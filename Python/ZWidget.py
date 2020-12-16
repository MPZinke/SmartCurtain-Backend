#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

###########################################################################
#
#	created by: MPZinke
#	on ..
#
#	DESCRIPTION:
#	BUGS:
#	FUTURE:
#
###########################################################################

from Properties import *;

import Logger;
from typing import Union;
from ZThread import ZThread;


class ZWidget:
	def __init__(self, name : str, sleep_time : Union[int, float]):
		self._has_changed_flag = True;  # indicate whether any of the (child) information has changed

		self._zthread = ZThread(name, self._loop_process, sleep_time);  # main driver of widget


	# ————————————————————— THREAD —————————————————————

	# Securely ends widget update.
	# Returns whether thread was successfully killed.
	def kill(self) -> None:
		try:
			self._zthread.kill();
			return True;
		except Exception as error:
			Logger.log_error(error);
			return False;

	# Checks if ZThread is still active.
	def is_alive(self) -> None:
		return self._zthread.is_alive();


	# Starts the ZThread.
	def start(self) -> None:
		self._zthread.start();


	# PLACEHOLDER: this is what is passed to the ZThread and is operated on.
	def _loop_process(self) -> None:
		raise Exception("ZWidget::_loop_process has not been overridden");


	# ————————————————————— DISPLAY —————————————————————

	# Returns whether the information has changed.
	def has_changed(self) -> None:
		return self._has_changed_flag;


	# PLACEHOLDER: this is what checks for differences in new and old values.
	def _mark_change_if_changed(self) -> None:
		raise Exception("ZWidget::_mark_change_if_changed has not been overridden");


	# Sets the has changed flag back to false after change has been updated.
	def update_displayed(self) -> None:
		self._has_changed_flag = False;
