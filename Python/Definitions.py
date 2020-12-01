#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

###########################################################################
#
#	created by: MPZinke
#	on 01.25.20
#
#	DESCRIPTION: Defined information for user and curtain.  Additionally contains functions
#		that are useful across multiple modules.
#	BUGS:
#	FUTURE:
#
###########################################################################

# —————————————— USER SPECIFIC EVENTS ——————————————

CITY = ""  #REQUIRED_EDIT
USER_FEED_KEY = ""  #REQUIRED_EDIT
USER_FEED_NAME = ""  #REQUIRED_EDIT
ALL_CURTAIN_FEED = {"open" : "all.curtain-open", "close" : "all.curtain-close"}


# ——————————————— DAYTIME EVENTS ————————————————

SAME_EVENT_TIME_DIFFERENCE_POSITION = 20
SAME_EVENT_TIME_DIFFERENCE_GENERIC = 10


# ————————————————— DATABASE ——————————————————

DB_NAME = "curtain"
DB_USER = "python_db_user"
DB_PASSWD = ""
DB_IP = "localhost"
DB_PORT = 3306


# ————————————————— ERROR LOG —————————————————

DELIMITER = '|'  # how values are sepparated in logs
ERROR_FILE_NAME = "ErrorLog.txt"


# ——————————————— EVENT PREDICTION ———————————————

CLUSTER_TIME_SPREAD = 1  # multiply by 2 for total diameter


# —————————————————— RPI.GPIO ——————————————————

# DIRECTION_PIN = 7
# PULSE_PIN = 11
# ENABLE_PIN = 13

# OPEN_STOP_PIN = 16
# CLOSED_STOP_PIN = 18

# PULSE_WAIT = .0000001


# —————————————————— SLEEP ———————————————————

ERROR_WAIT = 5
EVENT_PREDICTOR_SLEEP = 86400
# INTERVAL_BETWEEN_MANUAL_MOVEMENT_CHECKS = 10
# MOTOR_LOOP_RUN_WAIT = 1
SUNRISE_LOOP_WAIT = 86400
SUNSET_LOOP_WAIT = 86400


# ——————————————————— TIME ———————————————————

# time of day after which to put thread to sleep so that thread will activate at the beginning of 
# day.  This is so that if the thread calculates for current day only, it does not skip events: 
# EG. event predictor set events for today.  If it is activated past 12pm, and creates an event
# 9am, then that event will be skipped (or activated now)
HOUR_AFTER_WHICH_WAIT_UNTIL_NEXT_DAY_TO_RECALCULATE = 12

DATETIME_STRING_FORMAT = "%Y-%m-%d %H:%M:%S"
CLUSTER_SPAN = 4  # number of weeks looked back on to determine applicable logs


# —————————————————— OTHER ———————————————————

# STOPPED_PERCENT_LENIENCY = 5  # percentage of remaining steps before recalcuating


# —————————————————— SUGAR ———————————————————

# called to close and return from process in 1 line. EG
# >>> return close_cnx_and_return(cnx)
def close_cnx_and_return(cnx):
	cnx.close()
	return None


# used in if statements: check if value null; if null, sleep; return truthiness
def is_null_sleep_then(evalutated_value, sleep_amount=5):
	if not evalutated_value: sleep(sleep_amount)
	return not bool(evalutated_value)


# ————————————— THREAD SLEEP ALIGNMENT ——————————————

# bool value returned indicating if current time is past a defined time.  This time is used to
# determine if events might be missed because program start time is past event creation for
# day.  Used for program reseting
def current_time_is_past_sleep_point():
	from datetime import datetime

	today = datetime.today()
	sleep_point = datetime(year=today.year, month=today.month, day=today.day, 
				hour=HOUR_AFTER_WHICH_WAIT_UNTIL_NEXT_DAY_TO_RECALCULATE, 
				minute=0, second=0)
	return datetime.now() > sleep_point


def event_is_not_past_current_time(event_time):
	from datetime import datetime

	# time without timezone encoding
	naive_time = datetime(year=event_time.year, month=event_time.month, 
								day=event_time.day, hour=event_time.hour, 
								minute=event_time.minute, second=event_time.second)
	return naive_time > datetime.now()


# calculate the time to the next day if time is past a time that could cause missing events.
# returns the number of seconds until midnight +1 (as opposed to 24 hours)
def time_to_next_day():
	from datetime import datetime, timedelta

	today = datetime.today()
	beginning_of_day = datetime(year=today.year, month=today.month, day=today.day, 
									hour=0, minute=0, second=0)
	time_to_tomorrow_object = beginning_of_day + timedelta(days=1) - datetime.now()
	return time_to_tomorrow_object.seconds + 1  # for good measure


