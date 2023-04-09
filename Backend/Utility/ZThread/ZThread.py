#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"


########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.11.04                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE: Consider moving to multiprocessing::Process instead.                                                       #
#                                                                                                                      #
########################################################################################################################


from collections.abc import Callable;
from threading import Condition, Thread;
import warnings;
from warnings import warn as Warn;


from Utility import warning_message;
from Utility import Logger;


class ZThread(Thread):
	"""
	Modified thread class for executing a process and sleeping afterwards.
	Also allows for sleeping and waking a thread.
	"""
	def __init__(self, name : str, loop_process : Callable, sleep_time : Callable):
		Thread.__init__(self, name=name, target=self._thread_loop);

		self._condition = Condition();  # allows for sleep/wake feature
		self._is_active = True;  # used by thread_loop() for maintaining while loop
		self._loop_process = loop_process;  # operations special to child object
		self._sleep_time = sleep_time;  # function pointer to determine/return the amount of time it should sleep

		warnings.formatwarning = warning_message;


	def kill(self) -> None:
		"""
		SUMMARY: Ends a thread.
		DETAILS: Releases loop, wakes sleeping condition, joins thread with rest of program.
		"""
		if(not self._is_active and not self.is_alive()):
			raise Exception(f"Thread {self.name} is already killed");

		self._is_active = False;
		with self._condition:
			self._condition.notify();


	def set_sleep_time(self, sleep_time : Callable) -> None:
		"""
		SUMMARY: Changes the amount of time Condition::wait() will wait until next iteration.
		PARAMS:  Takes a function to determine the time ::_sleep_time will calculate. New sleep amount will begin after
		         current iteration on _thread_loop is complete.
		NOTES:   To implement immediately, follow with ::sleep(sleep_time()).
		"""
		self._sleep_time = sleep_time;


	def sleep(self, sleep_amount : int=0) -> None:
		"""
		SUMMARY: Sleeps thread_loop for amount of time.
		PARAMS:  Takes a numeric amount of time defaulted to None.
		NOTES: Sleeps for default amount of time if specified, otherwise indefinitely.
		"""
		with self._condition:
			if(sleep_amount):
				self._condition.wait(sleep_amount);
			else:
				Warn(f"Thread: {self.name} has been indefinitely put to sleep");
				self._condition.wait();  # incase 0 is used, default to indefinitely


	def _thread_loop(self) -> None:
		"""
		SUMMARY: Main loop that runs thread if activated.
		NOTES:   Check that the it is supposed to do stuff, then sleeps thread
		"""
		try:  # make it safe!!!
			while(self._is_active):
				self._loop_process();
				self.sleep(self._sleep_time());

		except Exception as error:
			try: Logger.log_error(error);
			except: pass;


	def wake(self) -> None:
		"""
		SUMMARY: Wakes thread (condition from sleep).
		"""
		if(not self._is_active):
			raise Exception("Waking a dead thread does nothing. Try using restart()");

		with self._condition:
			self._condition.notify();
