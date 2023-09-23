

import asyncio
from flask import render_template, session
import httpx


async def GET(home_id: int):
	async with httpx.AsyncClient() as client:
		home = (await client.get(f"http://localhost:8001/homes/{home_id}")).json()
	print(home)
	path = [{"path": f"""/homes/{home["id"]}""", "name": home["name"]}]
	return render_template("Home/Index.j2", home=home, path=path)
