#!/usr/bin/env python3
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

from collections.abc import Callable
from threading import Condition, Thread;
from warnings import warn as Warn;
from typing import Union;


# Modified thread class for executing a process and sleeping afterwards.
# Also allows for sleeping and waking a thread.
class ZThread(Thread):
	def __init__(self, name : str, loop_process : Callable, sleep_time):
		Thread.__init__(self, name=name, target=self._thread_loop);

		self._condition = Condition();  # allows for sleep/wake feature
		self._is_active = True;  # used by thread_loop() for maintaining while loop
		self._lock_skip_iteration_process = False;  # does not allow _skip_iteration_process to reset
		self._loop_process = loop_process;  # operations special to child object
		self._skip_iteration_process = False;  # option to skip the loop process for this iteration
		self._sleep_time = sleep_time;  # function pointer to determine/return the amount of time it should sleep


	# Ends a thread.
	# Releases loop, wakes sleeping condition, joins thread with rest of program.
	def kill(self) -> None:
		if(not self._is_active and not self.is_alive()): raise Exception("Thread is already killed");

		self._is_active = False;
		with self._condition: self._condition.notify();
		self.join();


	# Changes the amount of time Condition::wait() will wait until next iteration.
	# Takes the amount of time ::_sleep_time will equal.  New sleep amount will begin after current iteration
	# on _thread_loop is complete.
	def set_sleep_time(self, amount : Union[int, float]) -> None:
		self._sleep_time = amount;


	# Sets the sleep time and immediately sleeps for that amount of time.
	# Takes the amount of time ::_sleep_time will equal, whether loop process should be skipped (default: True).
	# Sets _sleep_time, then _skip_process to skip the process for this interation. Starts iteration on 
	# _thread_loop, skips process, then reinitializes process.
	def set_immediate_sleep_time(self, amount : Union[int, float], skip_iteration : bool=True) -> None:
		self._sleep_time = amount;
		self._skip_iteration_process = skip_iteration;
		self.wake();


	# Sleeps thread_loop for amount of time.
	# Takes a numeric amount of time defaulted to None.
	# Sleeps for default amount of time if specified, otherwise indefinitely.
	def sleep(self, amount : Union[int, float, None]=None) -> None:
		with self._condition:
			if(amount): self._condition.wait(amount);
			else:
				Warn(f"Thread: {self.name} has been indefinitely put to sleep");
				self._condition.wait();  # incase 0 is used, default to indefinitely


	# Main loop that runs thread if activated.
	# Check that the it is supposed to do stuff, then sleeps thread
	def _thread_loop(self) -> None:
		while(self._is_active):
			if(not self._skip_iteration_process): self._loop_process();
			if(not self._lock_skip_iteration_process): self._skip_iteration_process = False;
			self.sleep(self._sleep_time());


	# Wakes thread (condition from sleep).
	def wake(self) -> None:
		if(not self._is_active): raise Exception("Waking a dead thread does nothing. Try using restart()");
		with self._condition: self._condition.notify();
