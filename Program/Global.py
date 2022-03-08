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


from pathlib import Path;


# ———— Directories ————
# __file__ == "SmartCurtain/Hub/Program/Other/Global.py"
REPO_DIR = str(Path(__file__).absolute().parent.parent.parent);  # /usr/local/SmartCurtain
HUB_DIR = str(Path(__file__).absolute().parent.parent);  # /usr/local/SmartCurtain/Hub
DB_DIR = HUB_DIR+"/DB";  # /usr/local/SmartCurtain/Hub/DB
PYTHON_DIR = str(Path(__file__).absolute().parent);  # /usr/local/SmartCurtain/Hub/Program
# ———— Directories::Other ————
LOG_DIR = "/var/log/SmartCurtain"


NONETYPE = type(None);
