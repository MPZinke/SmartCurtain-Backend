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


import asyncio
from flask import render_template, session
import httpx


# —————————————————————————————————————————————————————— ROUTES —————————————————————————————————————————————————————— #

async def GET():
	async with httpx.AsyncClient() as client:
		homes = (await client.get("http://localhost:8001/homes")).json()
		print(homes)
	return render_template("Index.j2", homes=homes, path="")


def favicon():
	return ""
