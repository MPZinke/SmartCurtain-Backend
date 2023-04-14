

from datetime import datetime
import os
from sqlalchemy import create_engine, func, select, update, Boolean, Column, DateTime, ForeignKey, Integer, MetaData, Table
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import text
from typing import Optional


DB_USER: str = os.getenv("SMARTCURTAIN_DB_USER");
DB_HOST: str = os.getenv("SMARTCURTAIN_DB_HOST");
DB_PASSWORD: str = os.getenv("SMARTCURTAIN_DB_PASSWORD");


# ————————————————————————————————————————————————— OBJECT  CREATION ————————————————————————————————————————————————— #

# FROM: https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html
ENGINE = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/SmartCurtain", future=True)
BASE = automap_base()
METADATA = MetaData()

Table('HomesEventsView', BASE.metadata,
	Column('id', Integer, primary_key=True),
	Column("Events.id", Integer, ForeignKey("Events.id"), nullable=False),
	Column("Homes.id", Integer, ForeignKey("Homes.id"), nullable=False),
	Column("Options.id", Boolean, ForeignKey("Options.id"), nullable=False),
	Column("is_deleted", Boolean),
	Column("is_activated", Boolean),
	Column("percentage", Integer),
	Column("time", DateTime),
	autoload_with=ENGINE
)

Table('RoomsEventsView', BASE.metadata,
	Column('id', Integer, primary_key=True),
	Column("Events.id", Integer, ForeignKey("Events.id"), nullable=False),
	Column("Rooms.id", Integer, ForeignKey("Rooms.id"), nullable=False),
	Column("Options.id", Boolean, ForeignKey("Options.id"), nullable=False),
	Column("is_deleted", Boolean),
	Column("is_activated", Boolean),
	Column("percentage", Integer),
	Column("time", DateTime),
	autoload_with=ENGINE
)

Table('CurtainsEventsView', BASE.metadata,
	Column('id', Integer, primary_key=True),
	Column("Events.id", Integer, ForeignKey("Events.id"), nullable=False),
	Column("Curtains.id", Integer, ForeignKey("Curtains.id"), nullable=False),
	Column("Options.id", Boolean, ForeignKey("Options.id"), nullable=False),
	Column("is_deleted", Boolean),
	Column("is_activated", Boolean),
	Column("percentage", Integer),
	Column("time", DateTime),
	autoload_with=ENGINE
)

BASE.prepare(autoload_with=ENGINE)


Homes = BASE.classes.Homes
Rooms = BASE.classes.Rooms
Curtains = BASE.classes.Curtains

Options = BASE.classes.Options
HomesOptions = BASE.classes.HomesOptions
RoomsOptions = BASE.classes.RoomsOptions
CurtainsOptions = BASE.classes.CurtainsOptions

Events = BASE.classes.Events
HomesEvents = BASE.classes.HomesEvents
RoomsEvents = BASE.classes.RoomsEvents
CurtainsEvents = BASE.classes.CurtainsEvents

HomesEventsView = BASE.classes.HomesEventsView
RoomsEventsView = BASE.classes.RoomsEventsView
CurtainsEventsView = BASE.classes.CurtainsEventsView


def Homes__iter__(self) -> dict:
	print(dir(self))
	yield from {
		"id": self.id,
		"is_deleted": self.is_deleted,
		"name": self.name,
		"HomesEvents": list(map(dict, self.homeseventsview_collection)),
		"HomesOptions": list(map(dict, self.homesoptions_collection)),
		"Rooms": list(map(dict, self.rooms_collection))
	}.items()


def Rooms__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"is_deleted": self.is_deleted,
		"name": self.name,
		"RoomsEvents": list(map(dict, self.roomseventsview_collection)),
		"RoomsOptions": list(map(dict, self.roomsoptions_collection)),
		"Curtains": list(map(dict, self.curtains_collection))
	}.items()


def Curtains__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"buffer_time": self.buffer_time,
		"direction": self.direction,
		"is_deleted": self.is_deleted,
		"length": self.length,
		"name": self.name,
		"CurtainsEvents": list(map(dict, self.curtainseventsview_collection)),
		"CurtainsOptions": list(map(dict, self.curtainsoptions_collection))
	}.items()


def Options__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"description": self.description,
		"is_deleted": self.is_deleted,
		"name": self.name
	}.items()


def AreaOptions__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"Option": dict(self.options),
		"data": self.data,
		"is_on": self.is_on,
		"notes": self.notes
	}.items()


def Events__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"is_activated": self.is_activated,
		"percentage": self.percentage,
		"time": self.time,
		"Option": dict(self.options) if(self.options is not None) else None
	}.items()


def AreaEvents__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"is_deleted": self.is_deleted,
		"Event": dict(self.events) if(self.events is not None) else None
	}.items()


def AreaEventsView__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"is_deleted": self.is_deleted,
		"Option": dict(self.options) if(self.options is not None) else None,
		"is_deleted": self.is_deleted,
		"is_activated": self.is_activated,
		"percentage": self.percentage,
		"time": self.time
	}.items()


Homes.__iter__ = Homes__iter__
Rooms.__iter__ = Rooms__iter__
Curtains.__iter__ = Curtains__iter__


Events.__iter__ = Events__iter__
HomesEvents.__iter__ = AreaEvents__iter__
RoomsEvents.__iter__ = AreaEvents__iter__
CurtainsEvents.__iter__ = AreaEvents__iter__

Options.__iter__ = Options__iter__
HomesOptions.__iter__ = AreaOptions__iter__
RoomsOptions.__iter__ = AreaOptions__iter__
CurtainsOptions.__iter__ = AreaOptions__iter__

HomesEventsView.__iter__ = AreaEventsView__iter__
RoomsEventsView.__iter__ = AreaEventsView__iter__
CurtainsEventsView.__iter__ = AreaEventsView__iter__


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


def SELECT_HomesEventsView() -> list:
	with Session(ENGINE) as session:
		statement = select(HomesEventsView)
		return list(map(dict, session.scalars(statement)))


def SELECT_Homes_WHERE_Current() -> list:
	with Session(ENGINE) as session:
		# statement = select(Homes).join(Curtains).join(CurtainsEvents).where(CurtainsEvents.is_activated == False).where(CurtainsEvents.is_deleted == False)
		# return list(map(dict, session.scalars(statement)))
		return Homes.query.join(CurtainsEvents).filter(is_activated=False, is_deleted=False)


def UPDATE_CurtainsEvents(id: int, *, is_activated: Optional[bool]=None, is_deleted: Optional[bool]=None,
  percentage: Optional[int]=None, time: Optional[datetime]=None, **kwargs: dict
):
	if(any(key != "Option" for key in kwargs)):
		raise Exception(f"""{", ".join([key for key in kwargs if(key != "Option")])} are not allowed""")

	with Session(ENGINE) as session:
		statement = update(CurtainsEvents).where(CurtainsEvents.id == id)
		# if((curtain_event := session.scalar(select(CurtainsEvents))) is None):
		# 	raise Exception(f"Could not find CurtainsEvents by id {id}")

		if(is_activated is not None):
			statement = statement.values(is_activated=is_activated)
		if(is_deleted is not None):
			statement = statement.values(is_deleted=is_deleted)
		if(percentage is not None):
			statement = statement.values(percentage=percentage)
		if(time is not None):
			statement = statement.values(time=time)
		if("Option" in kwargs):
			statement = statement.values(**{"Options.id": kwargs["Option"]["id"]})

		session.execute(statement)
		session.commit()


def INSERT_Event(Area: str, *, percentage: int, time: Optional[datetime]=None, **kwargs: dict):
	assert(Area in ["Curtains", "Rooms", "Homes"]), f"Area arg must be 'Curtains', 'Rooms', 'Homes', not '{Area}'"

	allowed_kwargs = [f"{Area}.id", "Options.id"]
	if(any(key not in allowed_kwargs for key in kwargs)):
		raise Exception(f"""{", ".join([key for key in kwargs if(key not in allowed_kwargs)])} are not allowed""")

	if(time is None):
		time = datetime.now()


def INSERT_HomeEvent():
	test = HomesEventsView(**{
			"Homes.id": 1,
			"percentage": 1,
		}
	)
	with Session(ENGINE) as session:
		session.add(test)
		session.commit()


def test():
	# INSERT_HomeEvent()
	import json
	# print(json.dumps(SELECT_HomesEventsView(), default=str, indent=4))
	# INSERT_Event()
	print(json.dumps(SELECT_Homes(), default=str, indent=4))
	# print(json.dumps(SELECT_Homes_WHERE_Current(), default=str, indent=4))
	# UPDATE_CurtainsEvents(1, is_activated=True, is_deleted=True)


if(__name__ == "__main__"):
	test()
