#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

###########################################################################
#
#	created by: MPZinke
#	on 01.25.20
#
#	DESCRIPTION: Google Assistant (or other) activation using MQTT client from Adafruit.
#		Creates a client in the try-catch loop, subscribing to individual feeds from DB 
#		`options` table.  Once a message is received, it determines what kind of an event &
#		for what curtain it is using curtain_id_and_action_for_feed(.).  It then uses the event
#		type information to create an event in the DB.
#	BUGS:		-MQTTClient::connect() can fail without recording errors, but does not crash
#				 thread
#	FUTURE:	-Time based event creation
#
###########################################################################


from Adafruit_IO import MQTTClient
from time import sleep, time
from threading import Thread

from Definitions import *
import DBFunctions
import ErrorWriter

# —————————————————— UTILITY ——————————————————–

# return the `curtain_id` and action type for the desired feed name
def curtain_id_and_action_for_feed(feed_name):
	cnx, cursor = DBFunctions.connect_to_DB()
	feed_keys = DBFunctions.active_adafruit_feeds(cursor)
	cnx.close()

	for key in feed_keys:
		if feed_name == feed_keys[key]["open"]: return key, "open"
		if feed_name == feed_keys[key]["close"]: return key, "close"

	return None, None


# —————————————— ADAFRUIT CLIENT —————————————————

def connect_to_feeds(client):
	# subscribe to individual rooms
	cnx, cursor = DBFunctions.connect_to_DB()
	feeds = DBFunctions.active_adafruit_feeds(cursor)
	cnx.close()

	for key in feeds:
		if feeds[key]["open"]: client.subscribe(feeds[key]["open"])
		if feeds[key]["close"]: client.subscribe(feeds[key]["close"])

	# subscribe to all activating feeds
	for feed in ALL_CURTAIN_FEED:
		client.subscribe(ALL_CURTAIN_FEED[feed])


def disconnected(client):
	print("Adafruit Client Disconnected")
	raise Exception("MQTTClient disconnected")


def activate_message(client, feed_id, position_payload):
	from datetime import datetime

	try: position_percentage = int(position_payload)
	except: return

	cnx, cursor = DBFunctions.connect_to_DB()

	if feed_id == ALL_CURTAIN_FEED["open"]:
		DBFunctions.open_all_curtains(cnx, cursor, position_percentage)
	elif feed_id == ALL_CURTAIN_FEED["close"]:
		DBFunctions.close_all_curtains(cnx, cursor)
	else:
		curtain, action = curtain_id_and_action_for_feed(feed_id)
		if not curtain and not action: return close_cnx_and_return(cnx)  # id not recognized

		if action == "open":
			DBFunctions.open_immediate_event(cnx, cursor, curtain, position_percentage)
		elif action == "close":
			DBFunctions.close_immediate_event(cnx, cursor, curtain)

	cnx.close()


def subscribe(client, userdata, mid, granted_qos):
	pass



# thread called by Master.py
def start_client_loop():
	while True:
		try:
			client = MQTTClient(USER_FEED_NAME, USER_FEED_KEY)

			client.on_connect = connect_to_feeds
			client.on_disconnect = disconnected
			client.on_message = activate_message
			client.on_subscribe  = subscribe
			
			client.connect()
			client.loop_blocking()

		except Exception as error:
			try:
				import ErrorWriter
				ErrorWriter.write_error(error)
			except: pass
			sleep(ERROR_WAIT)


if __name__ == '__main__':
	start_client_loop()