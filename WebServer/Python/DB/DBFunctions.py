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


def __UTILITY__query(cursor : object, query : str, *params) -> list:
	if(len(params)): cursor.execute(query, params);
	else: cursor.execute(query);
	return cursor.fetchall();


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
