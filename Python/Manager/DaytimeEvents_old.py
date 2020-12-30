#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

###########################################################################
#
#	created by: MPZinke
#	on 01.25.20
#
#	DESCRIPTION: Daytime events include closing at sundown and opening at sunup.
#		These are set individually (sunset is sepparate from sunrise).  Each event setter has
#		its own thread created in Master.py with a try-catch loop to maintain process errors 
#		that may arrise.  The use of this module requires a CITY definition for geo-location
#		that is in the Astral library.  This information is then checked if any events are
#		scheduled soon to it (to prevent double scheduling).  If it nothing is there it will set the
#		event.
#	BUGS:
#	FUTURE:
#
###########################################################################

from time import sleep

from Definitions import *
import DBFunctions
import ErrorWriter


# —————————————————— SUNSET ——————————————————

def sunset_time():
	from astral import Astral

	astr_object = Astral()
	astr_object.solar_depression = "civil"
	return astr_object[CITY].sun(local=True)["sunset"]


# thread called by Master.py
def sunset_loop():
	while True:
		try:
			cnx, cursor = DBFunctions.connect_to_DB()

			for curtain in DBFunctions.curtain_ids(cursor):
				if DBFunctions.sunset_close(cursor, curtain):
					sunset = sunset_time()
					if is_null_sleep_then(sunset): continue
					# check if sunset event already set
					if not DBFunctions.event_set_at_approximate_time_with_range(cursor, curtain, range(0,1), sunset) \
					and event_is_not_past_current_time(sunset):
						DBFunctions.add_event(cnx, cursor, curtain, 0, sunset)

			cnx.close()
			if current_time_is_past_sleep_point(): sleep_time = time_to_next_day()
			else: sleep_time = SUNSET_LOOP_WAIT
			sleep(sleep_time)
		except Exception as error:
			try:
				import ErrorWriter
				ErrorWriter.write_error(error)
			except: pass
			sleep(ERROR_WAIT)



# —————————————————— SUNRISE ——————————————————

def sunrise_time():
	from astral import Astral

	astr_object = Astral()
	astr_object.solar_depression = "civil"
	return astr_object[CITY].sun(local=True)["sunrise"]


# thread called by Master.py
def sunrise_loop():
	while True:
		try:
			cnx, cursor = DBFunctions.connect_to_DB()

			for curtain in DBFunctions.curtain_ids(cursor):
				if DBFunctions.sunrise_open(cursor, curtain):
					sunrise = sunrise_time()
					if is_null_sleep_then(sunrise): continue
					open_position = DBFunctions.curtain_length(cursor, curtain)
					if not DBFunctions.event_set_at_approximate_time_with_range(cursor, curtain, range(1,open_position+1), sunrise) \
					and event_is_not_past_current_time(sunrise):
						DBFunctions.add_event(cnx, cursor, curtain, open_position, sunrise)

			cnx.close()
			if current_time_is_past_sleep_point(): sleep_time = time_to_next_day()
			else: sleep_time = SUNRISE_LOOP_WAIT
			sleep(sleep_time)
		except Exception as error:
			try:
				import ErrorWriter
				ErrorWriter.write_error(error)
			except: pass
			sleep(ERROR_WAIT)


if __name__ == '__main__':
	# sunrise_loop()
	sunset_loop()
