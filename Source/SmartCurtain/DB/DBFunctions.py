

from datetime import datetime, timedelta
from mpzinke import Generic
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from typing import Optional


from SmartCurtain.DB import (
	ENGINE,
	Homes,
	Rooms,
	Curtains,
	HomesEvents,
	RoomsEvents,
	CurtainsEvents,
	Options
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


def SELECT_Homes_WHERE_Current() -> list[Homes]:
	def is_valid(event: dict) -> bool:
		now_plus_1_second: datetime = datetime.now() + timedelta(seconds=1)
		return event["is_deleted"] is False and event["is_activated"] is False and event["time"] > now_plus_1_second

	with Session(ENGINE) as session:
		statement = select(Homes).where(Homes.is_deleted == False)
		homes = list(map(dict, session.scalars(statement)))

	for home in homes:
		home["HomesEvents"] = [event for event in home["HomesEvents"] if(is_valid(event))]
		home["HomesOptions"] = [option for option in home["HomesOptions"] if(option["is_deleted"] is False)]

		home["Rooms"] = [room for room in home["Rooms"] if(room["is_deleted"] is False)]
		for room in home["Rooms"]:
			room["RoomsEvents"] = [event for event in room["RoomsEvents"] if(is_valid(event))]
			room["RoomsOptions"] = [option for option in room["RoomsOptions"] if(option["is_deleted"] is False)]

			room["Curtains"] = [curtain for curtain in room["Curtains"] if(curtain["is_deleted"] is False)]
			for curtain in room["Curtains"]:
				curtain["CurtainsEvents"] = [event for event in curtain["CurtainsEvents"] if(is_valid(event))]

				curtain_options = curtain["CurtainsOptions"]
				curtain["CurtainsOptions"] = [option for option in curtain_options if(option["is_deleted"] is False)]

	return homes


@Generic
def UPDATE_Events(__args__: type, id: int, *, is_activated: Optional[bool]=None, is_deleted: Optional[bool]=None,
	percentage: Optional[int]=None, time: Optional[datetime]=None, **kwargs: dict
):
	Event = {"Home": HomesEvents, "Room": RoomsEvents, "Curtain": CurtainsEvents}[__args__[0].__name__]

	if(1 < len(kwargs) or (len(kwargs) == 1 and next(kwargs) != "Option.id")):
		raise KeyError(f"""Bad key(s) {", ".join([key for key in kwargs if(key != "Options.id")])}""")

	with Session(ENGINE) as session:
		statement = update(Event).where(Event.id == id)

		if(is_activated is not None):
			statement = statement.values(is_activated=is_activated)
		if(is_deleted is not None):
			statement = statement.values(is_deleted=is_deleted)
		if(percentage is not None):
			statement = statement.values(percentage=percentage)
		if(time is not None):
			statement = statement.values(time=time)
		if("Options.id" in kwargs):
			statement = statement.values(**{"Options.id": kwargs["Options.id"]})

		session.execute(statement)
		session.commit()


def INSERT_HomesEvents(*, percentage: int, **kwargs: dict) -> HomesEvents:
	return INSERT_Events[Homes](percentage=percentage, **kwargs)


def INSERT_RoomsEvents(*, percentage: int, **kwargs: dict) -> RoomsEvents:
	return INSERT_Events[Rooms](percentage=percentage, **kwargs)


def INSERT_CurtainsEvents(*, percentage: int, **kwargs: dict) -> CurtainsEvents:
	return INSERT_Events[Curtains](percentage=percentage, **kwargs)


@Generic
def INSERT_Events(__args__, *, percentage: int, time: Optional[datetime|str]=None, **kwargs: dict) \
  -> HomesEvents|RoomsEvents|CurtainsEvents:
	area = __args__[0].__name__
	Event = {"Home": HomesEvents, "Room": RoomsEvents, "Curtain": CurtainsEvents}[area]

	allowed_args = [f"{area}s.id", "Options.id"]
	if(any(key not in allowed_args for key in kwargs)):
		raise KeyError(f"""Bad key(s) {", ".join([key for key in kwargs if(key not in allowed_args)])}""")

	event_args = {f"{area}s.id": kwargs[f"{area}s.id"], "Options.id": kwargs.get("Options.id"),
	  "percentage": percentage, "time": (time or datetime.now())}

	event = Event(**event_args)
	with Session(ENGINE) as session:
		session.add(event)
		session.commit()
		session.refresh(event)

		return dict(event)
