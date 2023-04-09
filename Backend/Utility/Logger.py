#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.10.15                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime;
from json import dumps as json_dumps;
from sys import stderr;
import traceback;
from typing import Union;


from Global import LOG_DIR;


def log_error(error : Union[Exception, str]) -> bool:
	"""
	SUMMARY: Writes error to log file. If issue occurs writing error, error is sent to stderr along with previous
	         function call.
	PARAMS:  Takes error object or string.
	DETAILS: Tries to traceback error. Creates json error message. Writes error to log (or stderr).
	RETURNS: Returns whether successfully written to log.
	"""
	try:
		try:
			module = traceback.format_exc();
		except:
			module = "Unknown traceback";

		error_data = {"time": datetime.now().strftime("%H:%M:%S"), "module": module, "error": str(error)};
		error_message = json_dumps(error_data)+"\n";

		print(json_dumps(error_data, indent=4)+"\n");

		with open(f"{LOG_DIR}/{datetime.now().strftime('%Y.%m.%d')}.log", "a") as log:
			log.write(error_message);

		return True;

	except Exception as log_error_error:
		from inspect import stack;
		print(stack()[1][3]+": ", error, file=stderr);
		print(stack()[1][3]+": ", log_error_error, file=stderr);

		return False;
