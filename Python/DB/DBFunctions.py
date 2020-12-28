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

def Curtain(cursor : object, Curtain_id : int) -> dict:
	return __UTILITY__query(cursor, "SELECT * FROM `Curtains` WHERE `id` = %s;", Curtain_id)[0];


def Curtains(cursor : object) -> list:
	return __UTILITY__query(cursor, "SELECT * FROM `Curtains` ORDER BY `id` ASC;");


def CurtainsEvents(cursor : object, Curtain_id : int) -> list:
	query = "SELECT `CurtainsEvents`.*, `Options`.* FROM `CurtainsEvents` " \
			+ "LEFT JOIN `Options` ON `Options`.`id` = `CurtainsEvents`.`id` WHERE `Curtains.id` = %s;";
	return __UTILITY__query(cursor, query, Curtain_id);


def CurtainsEvents_current(cursor : object, Curtain_id : int) -> list:
	query = "SELECT `CurtainsEvents`.*, `Options`.* FROM `CurtainsEvents` \n \
			LEFT JOIN `Options` ON `Options`.`id` = `CurtainsEvents`.`id` \n \
			WHERE `Curtains.id` = %s AND `CurtainsEvents`.`is_current` = TRUE;";
	return __UTILITY__query(cursor, query, Curtain_id);


def Options(cursor : object) -> list:
	return __UTILITY__query(cursor, "SELECT * FROM `Options` ORDER BY `id` ASC;");


def CurtainsOptions(cursor : object, Curtain_id : int) -> list:
	query = "SELECT `CurtainsOptions`.*, `Options`.* FROM `CurtainsOptions` " \
			+ "JOIN `Options` ON `Options`.`id` = `CurtainsOptions`.`Options.id` " \
			+ "WHERE `CurtainsOptions`.`Curtains.id` = %s;";
	return __UTILITY__query(cursor, query, Curtain_id)


def ALL_Curtain_info(cursor : object, Curtain_id : int) -> list:
	curtain_info = [Curtain(cursor, Curtain_id)];
	curtain_info.append(CurtainsEvents_current(cursor, Curtain_id));
	curtain_info.append(CurtainsOptions(cursor, Curtain_id));

	return curtain_info;


# —————————————————————————————————————————————————————— SETTERS ——————————————————————————————————————————————————————

def new_Event(cnx, cursor, Curtain_id : int, Options_id : int, desired_position : int, time : object) -> bool:
	query =	"INSERT INTO `CurtainsEvents` (`Curtains.id`, `Options.id`, `desired_position`, `time`) VALUES" \
			+ "(%s, %s, %s, %s);"
	args = (Curtain_id, Options_id, desired_position, time.strftime("%Y-%m-%d %H:%M:%S"));
	return __UTILITY__insert(cnx, cursor, query, *args);
