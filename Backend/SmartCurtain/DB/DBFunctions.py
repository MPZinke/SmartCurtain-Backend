

from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from typing import Optional


from SmartCurtain.DB import (
	ENGINE,
	Homes,
	Rooms,
	Curtains,
	Events,
	HomesEvents,
	RoomsEvents,
	CurtainsEvents,
	Options,
	HomesOptions,
	RoomsOptions,
	CurtainsOptions,
	HomesEventsView,
	RoomsEventsView,
	CurtainsEventsView,
)


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


def INSERT_HomesEvents(*, percentage: int, **kwargs: dict) -> HomesEventsView:
	return INSERT_Events("Homes", percentage=percentage, **kwargs)


def INSERT_RoomsEvents(*, percentage: int, **kwargs: dict) -> RoomsEventsView:
	return INSERT_Events("Rooms", percentage=percentage, **kwargs)


def INSERT_CurtainsEvents(*, percentage: int, **kwargs: dict) -> CurtainsEventsView:
	return INSERT_Events("Curtains", percentage=percentage, **kwargs)


def INSERT_Events(area: str, *, percentage: int, **kwargs: dict) -> HomesEventsView|RoomsEventsView|CurtainsEventsView:
	View = {"Homes": HomesEventsView, "Rooms": RoomsEventsView, "Curtains": CurtainsEventsView}[area]
	
	allowed_args = [f"{area}.id", "Options.id", "time"]
	if(any(key not in allowed_args for key in kwargs)):
		raise Exception(f"""Bad key(s) {", ".join([key for key in kwargs if(key not in allowed_args)])}""")

	event_args = {f"{area}.id": kwargs[f"{area}.id"], "percentage": percentage}
	event_args.update({key: value for key, value in kwargs.items() if(key != f"{area}.id")})

	event = View(**event_args)
	with Session(ENGINE) as session:
		session.add(event)
		session.commit()
		session.refresh(event)

		return dict(event)


def test():
	import json
	print(json.dumps(INSERT_RoomsEvents(percentage=0, time="2020-01-01 00:00:00", **{"Rooms.id": 1}), default=str, indent=4))
	print(json.dumps(INSERT_HomesEvents(percentage=0, time="2020-01-01 00:00:00", **{"Homes.id": 1}), default=str, indent=4))
	print(json.dumps(SELECT_Homes(), default=str, indent=4))


if(__name__ == "__main__"):
	test()
