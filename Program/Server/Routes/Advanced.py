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


# /advanced/log/<string:log_filename>
def advanced_log__log_filename(self, log_filename: str):
	self.set_session_and_header();

	with open(os.path.join(LOG_DIR, log_filename), "r") as file:
		contents = "<br/>".join(file.readlines());

	return render_template("Advanced/Log.html", header=self._header, contents=contents);


# /advanced/logs
def advanced_logs(self):
	self.set_session_and_header();

	logs = [log for log in os.listdir(LOG_DIR) if(os.path.isfile(os.path.join(LOG_DIR, log)))];
	logs.sort(reverse=True)

	return render_template("Advanced/Logs.html", header=self._header, logs=logs);
