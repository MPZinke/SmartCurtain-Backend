#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

###########################################################################
#
#	created by: MPZinke
#	on 01.25.20
#
#	DESCRIPTION: Write an error to the specified text file.  If no function name is provided,
#		it creates the error traceback.  Then it writes the traceback, error message, & current
#		timestamp of the error
#	BUGS:
#	FUTURE:	-Have the outfile be a .log file
#
###########################################################################

from datetime import datetime

from Definitions import *


def write_error(error, module=None):
	try:
		if not module:
			import traceback
			module = traceback.format_exc().split("\n")[-4].strip()

		# change delimiter if exists
		error_message = str(error).replace(DELIMITER, ',' if ',' is not DELIMITER else ' ')
		current_timestamp = datetime.now().strftime(DATETIME_STRING_FORMAT)
		with open(ERROR_FILE_NAME, "a") as error_file:
			error_file.write("%s%c%s%c%s\n" % (	module, DELIMITER,
														error_message, DELIMITER, 
														current_timestamp))
	except: pass
