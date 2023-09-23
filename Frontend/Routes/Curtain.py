

import asyncio
from flask import render_template, request, session
import httpx


async def GET(curtain_id: int):
	async with httpx.AsyncClient() as client:
		curtain_request = client.get(f"http://localhost:8001/curtains/{curtain_id}")
		structure_request = client.get(f"http://localhost:8001/curtains/{curtain_id}/structure")
		curtain_response, structure_response = await asyncio.gather(curtain_request, structure_request)

	curtain = curtain_response.json()
	structure = structure_response.json()
	print(structure)
	path = [structure["home"], structure["room"], structure["curtain"]]
	return render_template("Curtain/Index.j2", curtain=curtain, path=path)


async def POST(curtain_id: int):
	percentage_range = request.form["AreaEvent.New.Modal-percentage_range-input"]
	if(request.form.get("AreaEvent.New.Modal-select_time-checkbox")):
		date = request.form["AreaEvent.New.Modal-date-input"]
		time = request.form["AreaEvent.New.Modal-time-input"]

	async with httpx.AsyncClient() as client:
		curtain_request = client.get(f"http://localhost:8001/curtains/{curtain_id}")
		structure_request = client.get(f"http://localhost:8001/curtains/{curtain_id}/structure")
		curtain_response, structure_response = await asyncio.gather(curtain_request, structure_request)
