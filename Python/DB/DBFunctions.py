#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on ..                                                                                                              #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################

from datetime import timedelta;


def __CONNECT__(user : str, password : str, db_name : str):
	import mysql.connector;
	cnx = mysql.connector.connect(user=user, password=password, host="localhost", port="3306",  database=db_name);
	return cnx, cnx.cursor(buffered=True);


def __UTILITY__associate_query(cursor):
	headers = [header[0] for header in cursor._description];
	return [{header : (row[x] if row[x] else None) for x, header in enumerate(headers)} for row in cursor._rows];


def __UTILITY__insert(cnx : object, cursor : object, query : str, *params) -> int:
	if(len(params)): cursor.execute(query, params);
	else: cursor.execute(query);
	if(not cnx.commit()): return 0;
	return cursor.lastrowid;


def __UTILITY__query(cursor : object, query : str, *params) -> list:
	if(len(params)): cursor.execute(query, params);
	else: cursor.execute(query);
	return __UTILITY__associate_query(cursor);



# —————————————————————————————————————————————————————— GETTERS ——————————————————————————————————————————————————————
# —————————————————————————————————————————————————— GETTERS: TABLES ——————————————————————————————————————————————————

def Curtain(cursor : object, Curtains_id : int) -> dict:
	curtain_info = __UTILITY__query(cursor, "SELECT * FROM `Curtains` WHERE `id` = %s;", Curtains_id);
	return curtain_info[0] if curtain_info else {};


def Curtains(cursor : object) -> list:
	return __UTILITY__query(cursor, "SELECT * FROM `Curtains` ORDER BY `id` ASC;");


def CurtainsEvents(cursor : object, Curtains_id : int) -> list:
	query = "SELECT `CurtainsEvents`.*, `Options`.* FROM `CurtainsEvents` " \
			+ "LEFT JOIN `Options` ON `Options`.`id` = `CurtainsEvents`.`id` WHERE `Curtains.id` = %s;";
	return __UTILITY__query(cursor, query, Curtains_id);


def CurtainsEvents_current(cursor : object, Curtains_id : int) -> list:
	query = "SELECT `CurtainsEvents`.*, `Options`.* FROM `CurtainsEvents` \n \
			LEFT JOIN `Options` ON `Options`.`id` = `CurtainsEvents`.`id` \n \
			WHERE `Curtains.id` = %s AND `CurtainsEvents`.`is_current` = TRUE;";
	return __UTILITY__query(cursor, query, Curtains_id);


def Options(cursor : object) -> list:
	return __UTILITY__query(cursor, "SELECT * FROM `Options` ORDER BY `id` ASC;");


def CurtainsOptions(cursor : object, Curtains_id : int) -> list:
	query = "SELECT `CurtainsOptions`.*, `Options`.* FROM `CurtainsOptions` " \
			+ "JOIN `Options` ON `Options`.`id` = `CurtainsOptions`.`Options.id` " \
			+ "WHERE `CurtainsOptions`.`Curtains.id` = %s;";
	return __UTILITY__query(cursor, query, Curtains_id);


# ————————————————————————————————————————————————— GETTERS: SPECIFIC —————————————————————————————————————————————————

def ALL_Curtain_info(cursor : object, Curtains_id : int) -> list:
	curtain_info = [Curtain(cursor, Curtains_id)];
	curtain_info.append(CurtainsEvents_current(cursor, Curtains_id));
	curtain_info.append(CurtainsOptions(cursor, Curtains_id));

	return curtain_info;


def Curtains_ids(cursor : object) -> list:
	return [curtain["id"] for curtain in __UTILITY__query(cursor, "SELECT `id` FROM `Curtains` ORDER BY `id` ASC;")];


def CurtainsEvents_for_curtain(cursor : object, Curtains_id : int) -> list:
	return __UTILITY__query(cursor, "SELECT * FROM `CurtainsEvents` WHERE `Curtains.id` = %s;", Curtains_id);


def CurtainsEvents_in_range_for_Options_id(cursor : object, Curtains_id : int, Options_id : int, time : object,
  minute_range : int) -> list:
	time_min = (time - timedelta(minutes=minute_range)).strftime("%Y-%m-%d %H:%M:%S");
	time_max = (time + timedelta(minutes=minute_range)).strftime("%Y-%m-%d %H:%M:%S");

	query = "SELECT * FROM `CurtainsEvents` WHERE `Curtains.id` = %s AND `Options.id` = %s " \
			+ "AND %s <= `time` AND `time` <= %s;";
	return __UTILITY__query(cursor, query, Curtains_id, Options_id, time_min, time_max);


def CurtainsOptions_for_curtain(cursor : object, Curtains_id : int) -> list:
	return __UTILITY__query(cursor, "SELECT * FROM `CurtainsOptions` WHERE `Curtains.id` = %s;", Curtains_id);


def CurtainsOptions_for_curtain_and_option(cursor : object, Curtains_id : int, Options_name : str) -> dict:
	query =	"SELECT * FROM `CurtainsOptions` LEFT JOIN `Options` ON `Options`.`id` = `CurtainsOptions`.`Options.id`" \
			+ "WHERE `CurtainsOptions`.`Curtains.id` = %s AND `Options`.`name` = %s;";
	curtain_option = __UTILITY__query(cursor, query, Curtains_id, Options_name);
	return curtain_option[0] if curtain_option else {};


def CurtainsOptionsKeyValues_for_CurtainsOptions_id(cursor : object, CurtainsOptions_id : id) -> list:
	query = "SELECT * FROM `CurtainsOptionsKeyValues` WHERE `CurtainsOptions.id` = %s";
	return __UTILITY__query(cursor, query, CurtainsOptions_id);


# —————————————————————————————————————————————————————— SETTERS ——————————————————————————————————————————————————————

def new_Event(cnx, cursor, Curtains_id : int, Options_id : int, desired_position : int, time : object) -> bool:
	query =	"INSERT INTO `CurtainsEvents` (`Curtains.id`, `Options.id`, `desired_position`, `time`) VALUES" \
			+ "(%s, %s, %s, %s);"
	args = (Curtains_id, Options_id, desired_position, time.strftime("%Y-%m-%d %H:%M:%S"));
	return __UTILITY__insert(cnx, cursor, query, *args);
