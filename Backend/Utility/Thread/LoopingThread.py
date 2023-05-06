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


from Utility.Thread import BaseThread


class LoopingThread(BaseThread):
	def __init__(self, name: str, *, action: callable, time: callable):
		BaseThread.__init__(self, name, action=self, time=time)


	def __call__(self):
		try:  # make it safe!!!
			while(self._is_active):
				self.action();
				self.sleep(self.time());

		except Exception as error:
			print(error)


def test():
	thread = LoopingThread("Test", action=lambda: print("Test"), time=lambda: 2)
	thread.start()


if(__name__ == "__main__"):
	test()
