#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.23                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from flask import render_template


# ——————————————————————————————————————————————————————— ROUTES ———————————————————————————————————————————————————————

async def index():
	return "<h1>Welcome!</h1>"


def favicon():
	return ""


def test():
	print(request.get_json())
	return "{\"success\":\"It worked\"}"
