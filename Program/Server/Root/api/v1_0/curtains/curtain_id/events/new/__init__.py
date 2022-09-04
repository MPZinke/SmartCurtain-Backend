#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.09.03                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from System import System;


# `POST /api/v1.0/curtain/<int:curtain_id>/events/new`
# Creates a new curtain's event with the JSON body.
def POST(system: System, curtain_id: int):
	return "TODO"