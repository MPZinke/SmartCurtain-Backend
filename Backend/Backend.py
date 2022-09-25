#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.29                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION: SmartCurtain class is the primary operational part of the Hub. Creates & controls submodules of Hub   #
#    (Manager, Server, & System). This script is invoked by the SmartCurtain Systemd Service.                          #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from Manager import Manager;
from Server import Server;
from SmartCurtain import SmartCurtain;


class Backend:
	"""
	The main object that holds the various parts of the backend.
	"""
	def __init__(self):
		self._SmartCurtain = SmartCurtain();
		self._Manager = Manager(self._SmartCurtain);
		self._Server = Server(self._SmartCurtain);


	def start(self):
		# self._Manager.start();
		self._Server.start();
		self._SmartCurtain.start();



def main():
	smartcurtain = Backend();
	smartcurtain.start();


if __name__ == '__main__':
	main();
