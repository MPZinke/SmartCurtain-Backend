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


from Other.Logger import log_error;
from typing import Union;
from Class.ZThread import ZThread;


class ZWidget:
	def __init__(self, name : str, sleep_time : Union[int, float]):
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
