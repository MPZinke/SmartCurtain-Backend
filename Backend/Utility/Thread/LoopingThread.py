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


from typing import Optional
import threading
import warnings


from Utility import warning_message;


class LoopingThread(threading.Thread):
	def __init__(self, name: str, *, action: callable, time: callable):
		threading.Thread.__init__(self, name=name, target=self)

		self.action: callable = action;  # operations special to child object
		self._condition: threading.Condition = threading.Condition();  # allows for sleep/wake feature
		self._is_active: bool = True;  # used by thread_loop() for maintaining while loop
		self.time: callable = time;  # function pointer to determine/return the amount of time it should sleep

		warnings.formatwarning = warning_message;


	def __call__(self):
		try:  # make it safe!!!
			while(self._is_active):
				self.action();
				self.sleep(self.time());

		except Exception as error:
			print(error)


	def __del__(self) -> None:
		if(self.is_alive()):
			self.kill()


	def kill(self) -> None:
		"""
		SUMMARY: Ends a thread.
		DETAILS: Releases loop, wakes sleeping condition, joins thread with rest of program.
		"""
		self._is_active = False;
		with self._condition:
			self._condition.notify();


	def sleep(self, seconds: Optional[int]=None) -> None:
		"""
		SUMMARY: Sleeps thread loop for amount of time.
		PARAMS:  Takes a numeric amount of time defaulted to None.
		NOTES: Sleeps for default amount of time if specified, otherwise indefinitely.
		"""
		with self._condition:
			if(seconds is None):
				warnings.warn(f"Thread: {self.name} has been indefinitely put to sleep");

			self._condition.wait(seconds)


	def wake(self) -> None:
		"""
		SUMMARY: Wakes thread (condition from sleep).
		"""
		with self._condition:
			self._condition.notify();


def test():
	thread = Thread("Test", action=lambda: print("Test"), time=lambda: 2)
	thread.start()


if(__name__ == "__main__"):
	test()
