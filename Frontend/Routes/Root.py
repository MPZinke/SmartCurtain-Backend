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


from flask import render_template, session
import httpx


# —————————————————————————————————————————————————————— ROUTES —————————————————————————————————————————————————————— #

async def index():
	async with httpx.AsyncClient() as client:
		homes = (await client.get("http://localhost:8001/homes")).json()
		print(homes)
	return render_template("Index.j2", homes=homes)


async def home(home_id: int):
	async with httpx.AsyncClient() as client:
		home = (await client.get(f"http://localhost:8001/homes/{home_id}")).json()
		print(home)
	return render_template("Home/Index.j2", home=home)


async def room(room_id: int):
	async with httpx.AsyncClient() as client:
		room = (await client.get(f"http://localhost:8001/rooms/{room_id}")).json()
		print(room)
	return render_template("Room/Index.j2", room=room)


async def curtain(curtain_id: int):
	async with httpx.AsyncClient() as client:
		curtain = (await client.get(f"http://localhost:8001/curtains/{curtain_id}")).json()
		print(curtain)
	return render_template("Curtain/Index.j2", curtain=curtain)


def favicon():
	return ""


def test():
	print(request.get_json())
	return "{\"success\":\"It worked\"}"
