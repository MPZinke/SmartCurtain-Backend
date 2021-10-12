#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

###########################################################################
#
#	created by: MPZinke
#	on 2020.10.15
#
#	DESCRIPTION:
#	BUGS:
#	FUTURE:
#
###########################################################################


from datetime import datetime;
from sys import stderr;
import traceback;
from typing import Union;

from Other.Global import SMARTCURTAIN_DIR;


# Writes error to log file. If issue occurs writing error, error is sent to stderr along with previous function call.
# Takes error object or string.
# Tries to traceback error. Creates pipe delimited error message. Writes error to log (or stderr).
# Returns whether successfully wrote to log
def log_error(error : Union[Exception, str]) -> bool:
	try:
		try: module = traceback.format_exc().split("\n")[-4].strip();
		except: module = "Unknown traceback";
		error_message = "%s|%s|%s\n" % (datetime.now().strftime("%H:%M:%S"), module, error);

		log_name = LOG_DIR+"/"+datetime.now().strftime("%Y.%m.%d")+".log";
		with open(log_name, "a") as log: log.write(error_message);
		print(error_message);
		return True;
	except Exception as log_error_error:
		from inspect import stack;
		print(stack()[1][3]+": ", error, file=stderr);
		return False;
