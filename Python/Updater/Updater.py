#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.10.07                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from Class.ZWidget import ZWidget;


class Updater(ZWidget):
	def __init__(self):
		ZWidget.__init__(self, "Updater", None);

		self.current_version;
		self.origin_Production_version;


	# Get current version from file


	# Download repo and `cd` into folder. Get origin Production version


	# Increment versions, checking for DB updates. If found, update DB


	# Run `make update` from folder


# CLI update function
