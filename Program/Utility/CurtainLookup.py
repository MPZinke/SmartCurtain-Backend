#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.05.16                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################

import os
import requests


def lookup_curtain(curtain_name: str) -> str:
	"""
	SUMMARY: Looks up the curtain from the NetworkIPLookup endpoint.
	PARAMS:  Takes the name of the curtain to lookup from NetworkIPLookup.
	DETAILS: Queries the NetworkIPLookup endpoint with the label for the curtain.
	RETURNS: The IP address string for the curtain.
	"""
	NetworkIPLookup_host = os.getenv("NETWORKIPLOOKUP_HOST")
	NetworkIPLookup_bearer_token = os.getenv("NETWORKIPLOOKUP_BEARERTOKEN")
	SmartCurtain_network_name = os.getenv("SMARTCURTAIN_NETWORKNAME")

	url = f"http://{NetworkIPLookup_host}/api/v1.0/network/label/{SmartCurtain_network_name}/ip/label/{curtain_name}"
	response = requests.get(url, headers={"Authorization": f"Bearer {NetworkIPLookup_bearer_token}"})

	if(response.status_code == 200):
		return response.json()["address"]

	return None
