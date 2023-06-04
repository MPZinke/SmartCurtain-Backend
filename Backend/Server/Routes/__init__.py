#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2023.05.11                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import json


from Server.Routes import homes
from Server.Routes import rooms
from Server.Routes import curtains
from SmartCurtain import SmartCurtain


def GET(smart_curtain: SmartCurtain):
	"""
	`GET /`
	"""
	# Uses `json.dumps` to keep order
	return json.dumps({
			"GET /": "List all backend's endpoints",

			# ———— HOMES ———— #
			"GET /homes": "List all homes",
			"POST /homes": "Add a new home",

			"GET /homes/<int:home_id>": "Show the info for a particular home",
			"DELETE /homes/<int:home_id>": "Delete a particular home",
			"PATCH /homes/<int:home_id>": "Update a particular home",
			"POST /homes/<int:home_id>": "Add a home event to a particular home",

			"GET /homes/<int:home_id>/rooms": "List all rooms for a particular home",
			"GET /homes/<int:home_id>/curtains": "List all curtains for a particular home",
			"GET /homes/<int:home_id>/events": "List all events for a particular home",

			# ———— ROOMS ———— #
			"GET /rooms": "List all rooms",
			"POST /rooms": "Adds a new room",

			"GET /rooms/<int:room_id>": "Show a particular room",
			"DELETE /rooms/<int:room_id>": "Delete a particular room",
			"PATCH /rooms/<int:room_id>": "Update a particular room",
			"POST /rooms/<int:room_id>": "Add a new room event to a particular room",

			"GET /rooms/<int:room_id>/curtains": "List all curtains for a particular room",
			"GET /rooms/<int:room_id>/events": "List all events for a particular room",

			# ———— CURTAINS ———— #
			"GET /curtains": "List all curtains",
			"POST /curtains": "Adds a new curtain",

			"GET /curtains/<int:curtain_id>": "Show the info for a particular curtain",
			"DELETE /curtains/<int:curtain_id>": "Delete a particular curtain",
			"PATCH /curtains/<int:curtain_id>": "Update a particular curtain",
			"POST /curtains/<int:curtain_id>": "Add a new curtain event to a particular curtain",

			"GET /curtains/<int:curtain_id>/events": "List all events for a particular curtain",

			# ———— EVENTS ———— #
			"GET /homes/events/<int:event_id>": "Gets a particular home event",
			"PATCH /homes/events/<int:event_id>": "Updates a particular home event",
			"DELETE /homes/events/<int:event_id>": "Deletes a particular home event",

			"GET /rooms/events/<int:event_id>": "Gets a particular room event",
			"PATCH /rooms/events/<int:event_id>": "Updates a particular room event",
			"DELETE /rooms/events/<int:event_id>": "Deletes a particular room event",

			"GET /curtains/events/<int:event_id>": "Gets a particular curtain event",
			"PATCH /curtains/events/<int:event_id>": "Updates a particular curtain event",
			"DELETE /curtains/events/<int:event_id>": "Deletes a particular curtain event"
		}, indent=4)
