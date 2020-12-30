#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.29                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from Server.Server import Server;
from System.System import System;
from DB.DBCredentials import *;
from DB.DBFunctions import __CONNECT__;


class SmartCurtain:
	def __init__(self):
		self._System = System();
		self._Server = Server(self._System);


	def start(self):
		self._Server.start();


	def dict(self):
		return {"_System" : self._System.dict()};


	def print(self, tab=0, next_tab=0):
		print('\t'*tab, "_System : ");
		self._System.print(tab+next_tab, next_tab);



def main():
	smartcurtain = SmartCurtain();
	smartcurtain.start();


if __name__ == '__main__':
	main();