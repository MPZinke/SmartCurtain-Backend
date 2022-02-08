#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.02.07                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from flask import redirect, render_template, request, session;
import os;


from Other.Global import LOG_DIR;
import Other.Logger as Logger;


# /advanced/log/<str:log_filename>
def advanced_log__id(self, log_filename: str):
	pass;


# /advanced/logs
def advanced_logs(self):
	header = self.set_session_and_header();

	logs = [os.path.join(LOG_DIR, log) for log in os.listdir(LOG_DIR) if(os.path.isfile(os.path.join(LOG_DIR, log)))];

	return render_template("Advanced/Logs.html", header=self._header, logs=logs);
