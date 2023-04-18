#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.03.07                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import os
from sqlalchemy import create_engine, Boolean, Column, DateTime, ForeignKey, Integer, Table
from sqlalchemy.ext.automap import automap_base


DB_USER: str = os.getenv("SMARTCURTAIN_DB_USER");
DB_HOST: str = os.getenv("SMARTCURTAIN_DB_HOST");
DB_PASSWORD: str = os.getenv("SMARTCURTAIN_DB_PASSWORD");


# ————————————————————————————————————————————————— OBJECT  CREATION ————————————————————————————————————————————————— #

# FROM: https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html
ENGINE = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/SmartCurtain", future=True)
BASE = automap_base()

# FROM: https://stackoverflow.com/a/61939524
# Table('HomesEventsView', BASE.metadata,
# 	Column('id', Integer, primary_key=True),
# 	Column("Homes.id", Integer, ForeignKey("Homes.id"), nullable=False),
# 	Column("is_activated", Boolean),
# 	Column("is_deleted", Boolean),
# 	Column("Options.id", Boolean, ForeignKey("Options.id"), nullable=False),
# 	Column("percentage", Integer),
# 	Column("time", DateTime),
# 	autoload_with=ENGINE
# )

# Table('RoomsEventsView', BASE.metadata,
# 	Column('id', Integer, primary_key=True),
# 	Column("Rooms.id", Integer, ForeignKey("Rooms.id"), nullable=False),
# 	Column("is_activated", Boolean),
# 	Column("is_deleted", Boolean),
# 	Column("Options.id", Boolean, ForeignKey("Options.id"), nullable=False),
# 	Column("percentage", Integer),
# 	Column("time", DateTime),
# 	autoload_with=ENGINE
# )

# Table('CurtainsEventsView', BASE.metadata,
# 	Column('id', Integer, primary_key=True),
# 	Column("Curtains.id", Integer, ForeignKey("Curtains.id"), nullable=False),
# 	Column("is_activated", Boolean),
# 	Column("is_deleted", Boolean),
# 	Column("Options.id", Boolean, ForeignKey("Options.id"), nullable=False),
# 	Column("percentage", Integer),
# 	Column("time", DateTime),
# 	autoload_with=ENGINE
# )

BASE.prepare(autoload_with=ENGINE)


Homes = BASE.classes.Homes
Rooms = BASE.classes.Rooms
Curtains = BASE.classes.Curtains

Options = BASE.classes.Options
HomesOptions = BASE.classes.HomesOptions
RoomsOptions = BASE.classes.RoomsOptions
CurtainsOptions = BASE.classes.CurtainsOptions

HomesEvents = BASE.classes.HomesEvents
RoomsEvents = BASE.classes.RoomsEvents
CurtainsEvents = BASE.classes.CurtainsEvents

# HomesEventsView = BASE.classes.HomesEventsView
# RoomsEventsView = BASE.classes.RoomsEventsView
# CurtainsEventsView = BASE.classes.CurtainsEventsView


def Homes__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"is_deleted": self.is_deleted,
		"name": self.name,
		"HomesEvents": list(map(dict, self.homesevents_collection)),
		"HomesOptions": list(map(dict, self.homesoptions_collection)),
		"Rooms": list(map(dict, self.rooms_collection))
	}.items()


def Rooms__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"is_deleted": self.is_deleted,
		"name": self.name,
		"RoomsEvents": list(map(dict, self.roomsevents_collection)),
		"RoomsOptions": list(map(dict, self.roomsoptions_collection)),
		"Curtains": list(map(dict, self.curtains_collection))
	}.items()


def Curtains__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"direction": self.direction,
		"is_deleted": self.is_deleted,
		"length": self.length,
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


def AreaOptions__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"Option": dict(self.options),
		"data": self.data,
		"is_on": self.is_on,
		"notes": self.notes
	}.items()


def AreaEvents__iter__(self) -> dict:
	yield from {
		"id": self.id,
		"is_activated": self.is_activated,
		"is_deleted": self.is_deleted,
		"Option": dict(self.options) if(self.options is not None) else None,
		"percentage": self.percentage,
		"time": self.time
	}.items()


Homes.__iter__ = Homes__iter__
Rooms.__iter__ = Rooms__iter__
Curtains.__iter__ = Curtains__iter__

HomesEvents.__iter__ = AreaEvents__iter__
RoomsEvents.__iter__ = AreaEvents__iter__
CurtainsEvents.__iter__ = AreaEvents__iter__

Options.__iter__ = Options__iter__
HomesOptions.__iter__ = AreaOptions__iter__
RoomsOptions.__iter__ = AreaOptions__iter__
CurtainsOptions.__iter__ = AreaOptions__iter__

# HomesEventsView.__iter__ = AreaEventsView__iter__
# RoomsEventsView.__iter__ = AreaEventsView__iter__
# CurtainsEventsView.__iter__ = AreaEventsView__iter__

