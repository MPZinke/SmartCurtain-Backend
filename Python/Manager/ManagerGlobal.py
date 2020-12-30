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



def __GLOBAL__set_options_names() -> dict:
	from DB.DBCredentials import *;
	from DB.DBFunctions import __CONNECT__, Options;

	_, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
	options = Options(cursor);

	return {options["name"] : options["id"] for option in options};


OPTIONS_ID_FOR_NAME = __GLOBAL__set_options_names();  # used so that only the name (easier to read) has to be HARDCODED