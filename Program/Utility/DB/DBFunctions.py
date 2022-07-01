#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.11.25                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION: DB Functions are named to indicate what kind of an operation they perform. This prefix also indicates #
#    that the imported function is a DB function.                                                                      #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################

from datetime import datetime, timedelta;
import os;
import psycopg2;
import psycopg2.extras
from typing import Any, Set;


DB_USER: str = os.getenv("SMARTCURTAIN_DB_USER");
DB_PASSWORD: str = os.getenv("SMARTCURTAIN_DB_PASSWORD");
assert(bool(DB_USER) is True), "'SMARTCURTAIN_DB_USER' cannot have a value that evaluates to False";


def connection_wrapper(function: callable) -> callable:
	"""
	SUMMARY: Wraps a DB function with calls to connect and closes the DB.
	PARAMS:  Takes the function that will be wrapped.
	RETURNS: The function pointer that wraps the function.
	"""
	def close(*args: list) -> None:
		for arg in args:
			arg.close();

	def wrapper(*args: list, **kwargs: dict) -> Any:
		"""
		DETAILS: Creates a connection.
		"""
		connection_string = f"host=localhost dbname=SmartCurtain user={DB_USER} password={DB_PASSWORD}";
		connection = psycopg2.connect(connection_string);
		connection.autocommit = True;  # Automatically commit changes to DB
		cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor);

		try:
			return_values: Any = function(cursor, *args, **kwargs);
		except Exception as error:
			close(cursor, cursor);
			raise error;

		close(cursor, cursor);
		return return_values;

	return wrapper


# —————————————————————————————————————————————————————— GETTERS ——————————————————————————————————————————————————————
# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# —————————————————————————————————————————————————— GETTERS::TABLES ——————————————————————————————————————————————————

@connection_wrapper
def SELECT_Curtains(cursor: object) -> list:
	cursor.execute("""SELECT * FROM "Curtains" ORDER BY "id" ASC;""");
	return [dict(row) for row in cursor];


@connection_wrapper
def SELECT_Options(cursor: object) -> list:
	cursor.execute("""SELECT * FROM "Options" ORDER BY "id" ASC;""");
	return [dict(row) for row in cursor];


# ————————————————————————————————————————————————— GETTERS::CURTAINS —————————————————————————————————————————————————

@connection_wrapper
def SELECT_Curtains_by_id(cursor: object, Curtains_id: int) -> dict:
	curtain_info = cursor.execute("""SELECT * FROM "Curtains" WHERE "id" = %s;""", Curtains_id);
	return curtain_info[0] if curtain_info else {};


def DB_ALL_Curtain_info(cursor: object, Curtains_id: int) -> list:
	curtain_info = [Curtain(cursor, Curtains_id)];
	curtain_info.append(SELECT_current_CurtainsEvents(cursor, Curtains_id));
	curtain_info.append(SELECT_CurtainsOptions(cursor, Curtains_id));

	return curtain_info;


@connection_wrapper
def SELECT_Curtains_ids(cursor: object) -> list:
	return [curtain["id"] for curtain in cursor.execute("""SELECT "id" FROM "Curtains" ORDER BY "id" ASC;""")];


# —————————————————————————————————————————————— GETTERS::CURTAINSEVENTS ——————————————————————————————————————————————

# def CurtainsEvents(cursor: object, Curtains_id: int) -> list:
# 	query = "SELECT "CurtainsEvents".*, "Options".* FROM "CurtainsEvents" " \
# 			+ "LEFT JOIN "Options" ON "Options"."id" = "CurtainsEvents"."id" WHERE "Curtains.id" = %s;";
# 	cursor.execute(query, Curtains_id);
# 	return [dict(row) for row in cursor];


@connection_wrapper
def SELECT_current_CurtainsEvents(cursor: object, Curtains_id: int) -> list:
	query =	"""
			SELECT * FROM "CurtainsEvents" 
			WHERE "Curtains.id" = %s AND "time" >= %s 
			AND "is_current" = TRUE AND "is_activated" = FALSE;
			""";
	cursor.execute(query, Curtains_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"));
	return [dict(row) for row in cursor];


@connection_wrapper
def SELECT_CurtainsEvents(cursor: object, CurtainsEvents_id: int) -> dict:
	event = cursor.execute("""SELECT * FROM "CurtainsEvents" WHERE "id" = %s""", CurtainsEvents_id);
	return event[0] if event else {};


@connection_wrapper
def SELECT_CurtainsEvents_for_curtain(cursor: object, Curtains_id: int) -> list:
	cursor.execute("""SELECT * FROM "CurtainsEvents" WHERE "Curtains.id" = %s;""", Curtains_id);
	return [dict(row) for row in cursor];


@connection_wrapper
def SELECT_CurtainsEvents_in_range_for_Options_id(cursor: object, Curtains_id: int, Options_id: int, time: object,
  minute_range: int) -> list:
	time_min = (time - timedelta(minutes=minute_range)).strftime("%Y-%m-%d %H:%M:%S");
	time_max = (time + timedelta(minutes=minute_range)).strftime("%Y-%m-%d %H:%M:%S");

	query =	"""
			SELECT * FROM "CurtainsEvents" 
			WHERE "Curtains.id" = %s AND "Options.id" = %s 
			AND %s <= "time" AND "time" <= %s;
			""";
	cursor.execute(query, Curtains_id, Options_id, time_min, time_max);
	return [dict(row) for row in cursor];


# —————————————————————————————————————————————— GETTERS::CURTAINSOPTIONS ——————————————————————————————————————————————

# def CurtainsOptions(cursor: object, Curtains_id: int) -> list:
# 	query = "SELECT "CurtainsOptions".*, "Options".* FROM "CurtainsOptions" " \
# 			+ "JOIN "Options" ON "Options"."id" = "CurtainsOptions"."Options.id" " \
# 			+ "WHERE "CurtainsOptions"."Curtains.id" = %s;";
# 	cursor.execute(query, Curtains_id);
# 	return [dict(row) for row in cursor];


@connection_wrapper
def SELECT_CurtainsOptions(cursor: object, Curtains_id: int) -> list:
	query =	"""
			SELECT "CurtainsOptions".*, "Options"."name" FROM "CurtainsOptions"
			JOIN "Options" ON "CurtainsOptions"."Options.id" = "Options"."id"  -- added for easier searching
			WHERE "Curtains.id" = %s;
			""";
	cursor.execute(query, Curtains_id);
	return [dict(row) for row in cursor];


@connection_wrapper
def SELECT_CurtainsOptions_for_curtain_and_option(cursor: object, Curtains_id: int, Options_name: str) -> dict:
	query =	"""
			SELECT * FROM "CurtainsOptions" 
			LEFT JOIN "Options" ON "Options"."id" = "CurtainsOptions"."Options.id"
			WHERE "CurtainsOptions"."Curtains.id" = %s 
			AND "Options"."name" = %s;
			""";
	curtain_option = cursor.execute(query, Curtains_id, Options_name);
	return curtain_option[0] if curtain_option else {};


# —————————————————————————————————————————————————————— SETTERS ——————————————————————————————————————————————————————
# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# —————————————————————————————————————————————————— SETTERS::CURTAIN ——————————————————————————————————————————————————

@connection_wrapper
def UPDATE_Curtains_is_activated(cursor, Curtains_id: int, activation: bool) -> bool:
	return Update(cursor, """UPDATE "Curtains" SET "is_activated" = %s WHERE "id" = %s""", activation, Curtains_id);


@connection_wrapper
def UPDATE_Curtains_percentage(cursor, Curtains_id: int, percentage: int) -> bool:
	return Update(cursor, """UPDATE "Curtains" SET "percentage" = %s WHERE "id" = %s;""", percentage, Curtains_id);


@connection_wrapper
def UPDATE_Curtains_direction(cursor, Curtains_id: int, direction: bool) -> bool:
	return Update(cursor, """UPDATE "Curtains" SET "direction" = %s WHERE "id" = %s;""", int(direction), Curtains_id);


@connection_wrapper
def UPDATE_Curtains_last_connection(cursor, Curtains_id: int, last_connection: object=None) -> bool:
	query = """UPDATE "Curtains" SET "last_connection" = %s WHERE "id" = %s;""";
	if(not last_connection): last_connection = datetime.now();
	return bool(cursor.execute(query, last_connection, Curtains_id));


@connection_wrapper
def UPDATE_Curtains_ip_address(cursor, Curtains_id: int, ip_address: int) ->bool:
	Update(cursor, """UPDATE "Curtains" SET "ip_address" = %s WHERE "id" = %s;""", ip_address, Curtains_id);


@connection_wrapper
def UPDATE_Curtains_length(cursor, Curtains_id: int, length: int) ->bool:
	Update(cursor, """UPDATE "Curtains" SET "length" = %s WHERE "id" = %s;""", length, Curtains_id);


@connection_wrapper
def UPDATE_Curtains_name(cursor, Curtains_id: int, name: str) -> bool:
	Update(cursor, """UPDATE "Curtains" SET "name" = %s WHERE "id" = %s;""", name, Curtains_id);


# —————————————————————————————————————————————— SETTERS::CURTAINSEVENTS ——————————————————————————————————————————————

def INSERT_CurtainsEvents(cursor, Curtains_id: int, Options_id: int, percentage: int, time: object) -> bool:
	query =	"""
			INSERT INTO "CurtainsEvents" ("Curtains.id", "Options.id", "percentage", "time") VALUES
			(%s, %s, %s, %s)
			RETURNING "id";
			"""
	cursor.execute(query, (Curtains_id, Options_id, percentage, time.strftime("%Y-%m-%d %H:%M:%S")));
	return [dict(row) for row in cursor];


def Update(cursor, query: str, *args: Set[Any]) -> Any:
	cursor.execute(query, args);
	return bool(cursor.rowcount);


@connection_wrapper
def UPDATE_all_CurtainsEvents_is_activated(cursor) -> bool:
	Update(cursor, """UPDATE "CurtainsEvents" SET "is_activated" = TRUE;""");


@connection_wrapper
def UPDATE_all_prior_CurtainsEvents_is_activated(cursor) -> int:
	Update(cursor, """UPDATE "CurtainsEvents" SET "is_activated" = TRUE WHERE "time" < %s;""", datetime.now());


@connection_wrapper
def UPDATE_CurtainsEvents_percentage(cursor, CurtainsEvents_id: int, percentage: bool) -> bool:
	Update(cursor, """UPDATE "CurtainsEvents" SET "percentage" = %s WHERE "id" = %s""", percentage, CurtainsEvents_id);


@connection_wrapper
def UPDATE_CurtainsEvents_is_activated(cursor, CurtainsEvents_id: int, is_activated: bool) -> bool:
	Update(cursor, """UPDATE "CurtainsEvents" SET "is_activated" = %s WHERE "id" = %s""", is_activated,
	  CurtainsEvents_id);


@connection_wrapper
def UPDATE_CurtainsEvents_is_current(cursor, CurtainsEvents_id: int, is_current: bool) -> bool:
	Update(cursor, """UPDATE "CurtainsEvents" SET "is_current" = %s WHERE "id" = %s""", is_current, CurtainsEvents_id);


@connection_wrapper
def UPDATE_CurtainsEvents_time(cursor, CurtainsEvents_id: int, time: bool) -> bool:
	Update(cursor, """UPDATE "CurtainsEvents" SET "time" = %s WHERE "id" = %s""", time, CurtainsEvents_id);


# ————————————————————————————————————————————— SETTERS::CURTAINSOPTIONS ————————————————————————————————————————————— #

@connection_wrapper
def UPDATE_CurtainsOptions_is_on(cursor, CurtainsOptions_id: int, is_on: bool) -> bool:
	Update(cursor, """UPDATE "CurtainsOptions" SET "is_on" = %s WHERE "id" = %s;""", is_on, CurtainsOptions_id);


@connection_wrapper
def UPDATE_CurtainsOptions_notes(cursor, CurtainsOptions_id: int, notes: str) -> bool:
	Update(cursor, """UPDATE "CurtainsOptions" SET "notes" = %s WHERE "id" = %s;""", notes, CurtainsOptions_id);



@connection_wrapper
def UPDATE_CurtainsOptionsKeyValue_is_current(cursor, CurtainsOptions_id: int, is_current: bool) -> bool:
	Update(cursor, """UPDATE "CurtainsOptions" SET "is_current" = %s WHERE "id" = %s;""", is_current,
	  CurtainsOptions_id);


@connection_wrapper
def UPDATE_CurtainsOptionsKeyValue_key(cursor, CurtainsOptions_id: int, key: bool) -> bool:
	Update(cursor, """UPDATE "CurtainsOptions" SET "key" = %s WHERE "id" = %s;""", key, CurtainsOptions_id);


@connection_wrapper
def UPDATE_CurtainsOptionsKeyValue_value(cursor, CurtainsOptions_id: int, value: bool) -> bool:
	Update(cursor, """UPDATE "CurtainsOptions" SET "value" = %s WHERE "id" = %s;""", value, CurtainsOptions_id);
