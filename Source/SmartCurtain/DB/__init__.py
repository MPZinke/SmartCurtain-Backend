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
from pymongo import MongoClient


assert(DB_USER := os.getenv("SMARTCURTAIN_DB_USER")), "'SMARTCURTAIN_DB_USER' cannot evaluate to False"
assert(DB_HOST := os.getenv("SMARTCURTAIN_DB_HOST")), "'SMARTCURTAIN_DB_HOST' cannot evaluate to False"
assert((DB_PASSWORD := os.getenv("SMARTCURTAIN_DB_PASSWORD")) is not None), \
"'SMARTCURTAIN_DB_PASSWORD' is missing from environment"


SMART_CURTAIN_DATABASE = MongoClient(f"""mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/SmartCurtain""").SmartCurtain
