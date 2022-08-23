#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.23                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime, timedelta;
from flask import redirect, render_template, request, session;


from Server.ServerGlobal import *;
from Server.ServerGlobal import posted;
from Server.Utility import Header;
import Utility.Logger as Logger;
from Utility import try_convert;


# —————————————————————————————————————————————————————— INDEX  —————————————————————————————————————————————————————— #

def index(self):
	self.set_session_and_header()

	if(request.method == "POST"):
		return self.index_POST();

	return render_template("Home.html", header=self._header, session=session);


def index_POST(self):
	try:
		header = self._header;

		if(posted("open_button")):
			header.selected_curtain().open();
		elif(posted("close_button")):
			header.selected_curtain().close();
		elif(posted("set_button")):
			percentage = int(request.form["percentage_input"])
			header.selected_curtain().open(percentage);
			session["success"] = "Successfully created event";

	except Exception as error:
		Logger.log_error(error);
		session["error"] = f"Error setting event {str(error)}";

	return redirect("/");


# ——————————————————————————————————————————————————————— EDIT ——————————————————————————————————————————————————————— #

def edit(self):
	self.set_session_and_header()

	return render_template("Edit.html", header=self._header, session=session);


# —————————————————————————————————————————————————————— EVENTS —————————————————————————————————————————————————————— #

def events(self):
	self.set_session_and_header()

	if(request.method == "POST"):
		self.events_POST();

	return render_template("Events.html", header=self._header, session=session);


def events_POST(self):
	try:
		header = self._header;

		if(not (event_id := try_convert(*get_posted_value("event_id"), int)) or not isinstance(event_id, int)):
			raise Exception(f"{event_id} is not of correct type int");

		curtain = header.selected_curtain();
		event = curtain.CurtainEvent(id=event_id);
		event.delete();

	except Exception as error:
		Logger.log_error(error);
		session["error"] = f"Error setting event {str(error)}";


# ——————————————————————————————————————————————————————— NEW  ——————————————————————————————————————————————————————— #

def new(self):
	self.set_session_and_header();

	if(request.method == "POST"):
		return self.new_POST();

	return self.new_GET();


def new_GET(self):
	kwargs = {"header": self._header, "session": session};

	current_date = datetime.now().strftime("%Y-%m-%d");
	time_plus_hour = (datetime.now() + timedelta(hours=1)).strftime("%H:%M");
	kwargs = {**kwargs, "current_date": current_date, "time_plus_hour": time_plus_hour};
	return render_template("New.html", **kwargs);


def new_POST(self):
	try:
		if(posted("date_input") and posted("time_input") and posted("percentage_input")):
			date_input, time_input, percentage_input = get_posted_value("date_input", "time_input", "percentage_input");
			date_time = datetime.strptime(f"{date_input} {time_input}", "%Y-%m-%d %H:%M");
			percentage = int(percentage_input);

			self._header.selected_curtain().open(percentage, time=date_time);
			session["success"] = f"Successfully created event for {date_input} {time_input} at {percentage}";

		elif(not posted("date_input")):
			raise Exception("Value date_input not found");
		elif(not posted("time_input")):
			raise Exception("Value time_input not found");
		elif(not posted("percentage_input")):
			raise Exception("Value percentage_input not found");

	except Exception as error:
		Logger.log_error(error);
		session["error"] = f"Error setting event {str(error)}";

	return redirect("/new");


# —————————————————————————————————————————————————————— FAVICON —————————————————————————————————————————————————————— #

def favicon(self):
	return "";
