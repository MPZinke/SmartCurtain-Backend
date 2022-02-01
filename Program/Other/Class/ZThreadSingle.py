#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.09.14                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION: Created to sepparate the crazy logic between repeating and single occurance threads. The flow of this #
#    class is Sleep -> Action, where as the repeating class is (Action -> Sleep) <- REPEAT.                            #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from collections.abc import Callable;

from Other.Class.ZThread import ZThread;
import Other.Logger as Logger;



class ZThreadSingle(ZThread):
	def __init__(self, name : str, loop_process : Callable, sleep_time : Callable):
		ZThread.__init__(self, name, loop_process, sleep_time);


	# Main loop that runs thread if activated.
	# Check that the it is supposed to do stuff, then sleeps thread
	def _thread_loop(self) -> None:
		try:  # make it safe!!!
			self.sleep(self._sleep_time());
			if(self._is_active):
				self._loop_process();
		except Exception as error:
			try: Logger.log_error(error);
			except: pass;
