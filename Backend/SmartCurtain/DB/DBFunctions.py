

import os
from sqlalchemy import create_engine, func, select, MetaData
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.automap import automap_base
from typing import Optional


DB_USER: str = os.getenv("SMARTCURTAIN_DB_USER");
DB_HOST: str = os.getenv("SMARTCURTAIN_DB_HOST");
DB_PASSWORD: str = os.getenv("SMARTCURTAIN_DB_PASSWORD");


# ————————————————————————————————————————————————— OBJECT  CREATION ————————————————————————————————————————————————— #

# FROM: https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html
ENGINE = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/SmartCurtain")
Base = automap_base()
Base.prepare(autoload_with=ENGINE)


Homes = Base.classes.Homes
Rooms = Base.classes.Rooms
Curtains = Base.classes.Curtains
Options = Base.classes.Options
CurtainsEvents = Base.classes.CurtainsEvents
CurtainsOptions = Base.classes.CurtainsOptions


def Homes__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"is_deleted": self.is_deleted,
		"name": self.name,
		"Rooms": list(map(dict, self.rooms_collection))
	}.items()


def Rooms__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"is_deleted": self.is_deleted,
		"name": self.name,
		"Curtains": list(map(dict, self.curtains_collection))
	}.items()


def Curtains__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"buffer_time": self.buffer_time,
		"is_deleted": self.is_deleted,
		"name": self.name,
		"CurtainsEvents": list(map(dict, self.curtainsevents_collection)),
		"CurtainsOptions": list(map(dict, self.curtainsoptions_collection))
	}.items()


def Options__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"description": self.description,
		"is_deleted": self.is_deleted,
		"name": self.name
	}.items()


def CurtainsOptions__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"Option": dict(self.options),
		"data": self.data,
		"is_on": self.is_on,
		"notes": self.notes
	}.items()



def CurtainsEvents__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"is_activated": self.is_activated,
		"is_deleted": self.is_deleted,
		"percentage": self.percentage,
		"time": self.time,
	}.items()


Homes.__iter__ = Homes__iter__
Rooms.__iter__ = Rooms__iter__
Curtains.__iter__ = Curtains__iter__
Options.__iter__ = Options__iter__
CurtainsEvents.__iter__ = CurtainsEvents__iter__
CurtainsOptions.__iter__ = CurtainsOptions__iter__


def SELECT_Homes() -> list:
	with Session(ENGINE) as session:
		statement = select(Homes)
		return list(map(dict, session.scalars(statement)))


def SELECT_Rooms() -> list:
	with Session(ENGINE) as session:
		statement = select(Rooms)
		return list(map(dict, session.scalars(statement)))


def SELECT_Curtains() -> list:
	with Session(ENGINE) as session:
		statement = select(Curtains)
		return list(map(dict, session.scalars(statement)))


def SELECT_Options() -> list:
	with Session(ENGINE) as session:
		statement = select(Options)
		return list(map(dict, session.scalars(statement)))


def test():
	import json
	print(json.dumps(SELECT_Homes(), default=str, indent=4))


if(__name__ == "__main__"):
	test()
