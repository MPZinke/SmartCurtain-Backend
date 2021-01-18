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


from datetime import datetime, timedelta;
from os import getcwd as __OS__getcwd;
from pathlib import Path as __pathlib__Path;
import sys;


SMARTCURTAIN_DIR = str(__pathlib__Path(__OS__getcwd()));



# Get the datetime object for the next day at 00:00:00.
# Compliments of https://jacobbridges.github.io/post/how-many-seconds-until-midnight/
def tomorrow_00_00():
	tomorrow = datetime.now() + timedelta(1);
	return datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=0, minute=0, second=0);

