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

async def index():
	async with httpx.AsyncClient() as client:
		homes = (await client.get("http://localhost:8001/homes")).json()
		print(homes)
	return render_template("Index.j2", homes=homes, path="")


async def home(home_id: int):
	async with httpx.AsyncClient() as client:
		home = (await client.get(f"http://localhost:8001/homes/{home_id}")).json()
	print(home)
	path = [{"path": f"""/homes/{home["id"]}""", "name": home["name"]}]
	return render_template("Home/Index.j2", home=home, path=path)


async def room(room_id: int):
	async with httpx.AsyncClient() as client:
		room_request = client.get(f"http://localhost:8001/rooms/{room_id}")
		structure_request = client.get(f"http://localhost:8001/rooms/{room_id}/structure")
		room_response, structure_response = await asyncio.gather(room_request, structure_request)

	room = room_response.json()
	structure = structure_response.json()
	print(structure)
	path = [structure["home"], structure["room"]]
	return render_template("Room/Index.j2", room=room, path=path)


async def curtain(curtain_id: int):
	async with httpx.AsyncClient() as client:
		curtain_request = client.get(f"http://localhost:8001/curtains/{curtain_id}")
		structure_request = client.get(f"http://localhost:8001/curtains/{curtain_id}/structure")
		curtain_response, structure_response = await asyncio.gather(curtain_request, structure_request)

	curtain = curtain_response.json()
	structure = structure_response.json()
	print(structure)
	path = [structure["home"], structure["room"], structure["curtain"]]
	return render_template("Curtain/Index.j2", curtain=curtain, path=path)


def favicon():
	return ""


def test():
	print(request.get_json())
	return "{\"success\":\"It worked\"}"
