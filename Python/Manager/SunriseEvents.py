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


from DB.DBCredentials import *;
from DB.DBFunctions import __CONNECT__, Curtains_ids, CurtainsOptions_for_curtain_and_option;
from ManagerGlobal import *;
from Other.Global import *;
from ZWidget import ZWidget;


class SunriseEvents(ZWidget):
	def __init__(self):
		ZWidget.__init__(self, "SunriseEvents", SUNRISEEVENTS_SLEEP);


	def sunrise_time(self):
		from astral import Astral

		astr_object = Astral()
		astr_object.solar_depression = "civil"
		return astr_object[CITY].sun(local=True)["sunrise"]


	def _loop_process(self):
		cnx, cursor = __CONNECT__(DB_USER, DB_PASSWORD, DATABASE);
		try:
			for curtain in Curtains_ids(cursor):
				option_id = OPTIONS_ID_FOR_NAME["Sunrise Open"];  # name is HARDCODED
				curtain_option = CurtainsOptions_for_curtain_and_option(cursor, curtain["id"], "Sunrise Open");
				if not curtain_option or not curtain_option["is_on"]: continue;  # ignore if either not setup or not on

				if(CurtainsOptions_for_curtain_and_option(curtain["id"], curtain_option["id"], ))






def main():


if __name__ == "__main__":
	main()
