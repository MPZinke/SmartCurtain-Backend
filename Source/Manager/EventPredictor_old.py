#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

###########################################################################
#
#	created by: MPZinke
#	on ..
#
#	DESCRIPTION: K-Means clustering is used to determine possible events for day based
#		on events for that particular day of week for the last 4 weeks (hard coded).  Events 
#		contain the datetime object pulled from the DB, and converts it to a decimal 
#		representation of it for smoother calculation  A centroid is created for the ceil(average
#		number of events for that weekdat).  This centroid then finds its surrounding event 
#		times over 20 iterations or once all the centroid averages remain constant over 2 
#		iterations.  Each centroid then checks if it is valid—3 events within ±30 minutes 
#		(hardcoded) of the average.  Commented is code that will find the tightest grouping & 
#		check that it is valid, however it is deemed as unnecessary at the moment.  If a 
#		centroid is valid, it will average the position of each event and create a new event at
#		that position average.
#	BUGS:
#	FUTURE:
#
###########################################################################

from datetime import datetime, timedelta
from math import ceil
from time import sleep

import DBFunctions

from Definitions import *


# —————————————————— UTILITY ———————————————————

def sum_events(event_list):
	return sum([event.decimal for event in event_list])


# ————————————————— OBJECTS ———————————————————

class EventTime:
	def __init__(self, datetime_obj, position):
		self.datetime = datetime_obj
		self.decimal = self.datetime.hour + self.datetime.minute / 60
		self.position = position


class Centroid:
	def __init__(self, center, events):
		self.events = events
		self.center = center

	def finished(self, events):
		self.events = events
		if not len(events): return True
		new_center = sum_events(events) / len(events)
		if new_center == self.center: return True
		self.center = new_center
		return False

	def event_average(self):
		return sum([event.position for event in self.events]) / len(self.events)

	# check if 3 <= events are within an hour; reassign center for all valid events
	def is_valid(self):
		self.events = [event for event in self.events if self.center - .5 <= event.decimal <= self.center + .5]
		if len(self.events) < 3: return False
		self.center = sum_events(self.events) / len(self.events)
		return True
		# alternative way to do it with more adaptive surrounding points
		# while True:
		# 	surrounding_times = self.times_surrounding_average()
		# 	avg_of_surroundings = sum(surrounding_times) / len(surrounding_times)
		# 	if avg_of_surroundings == self.avg: break
		# 	self.avg = avg_of_surroundings
		# if len(surrounding_times) > 2: return True
		# return False


# —————————————— INITIALIZE VALUES —————————————————

# divide events evenly into groups for each centroid
# EG [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] => [[1, 2, 3], [4, 5, 6], [7, 8, 9, 10]]
def initial_groups(events):
	number_of_centroids = int(ceil(len(events) / 4))
	if not number_of_centroids: return []  # division by 0 error prevention

	initial_centroid_lists = [[] for x in range(number_of_centroids)]
	events_per_centroid = int(len(events) / number_of_centroids)
	last_index = 0
	# place evenly divisible amounts into arrays EG [[1, 2, 3], [4, 5, 6]]
	for x in range(number_of_centroids-1):
		for y in range(x * events_per_centroid, (x + 1) * events_per_centroid):
			initial_centroid_lists[x].append(events[y])
			last_index = y
	# place rest into last array EG , [7, 8, 9, 10]]
	for x in range(last_index, len(events)):
		initial_centroid_lists[-1].append(events[x])

	return initial_centroid_lists


# calculate average number of events for day and make centroids
def initialize_initial_centroids(initial_centroid_lists):
	initial_centroids = []
	for x in range(len(initial_centroid_lists)):
		avg = sum_events(initial_centroid_lists[x]) / len(initial_centroid_lists[x])
		initial_centroids.append(Centroid(avg, initial_centroid_lists[x]))

	return initial_centroids


# —————————————— CENTROID ASSIGNMENT ——————————————

def all_events_assigned_to_correct_centroids(centroids, centroid_event_lists):
	all_events_are_set = True
	for x in range(len(centroids)):
		if not centroids[x].finished(centroid_event_lists[x]): all_events_are_set = False
	return all_events_are_set


# return index of the closes centroid for a given event
def closest_centroid_index(event, centroids):
	closest_index = 0
	for x in range(1, len(centroids)):
		if abs(centroids[x].center - event.decimal) < abs(centroids[closest_index].center - event.decimal):
			closest_index = x
	return closest_index


def k_means(events, initial_centroid_lists):
	centroids = initialize_initial_centroids(initial_centroid_lists)

	max_iterations = 20
	while max_iterations:
		centroid_event_lists = [[] for x in range(len(centroids))]
		for event in events:
			centroid_event_lists[closest_centroid_index(event, centroids)].append(event)

		if all_events_assigned_to_correct_centroids(centroids, centroid_event_lists): break
		max_iterations -= 1

	return centroids


# ———————————————— EVENT CREATION ———————————————

# create event objects for predicted events using centroid time avg & ::events position avg
def create_new_events(centroids):
	today = datetime.today()
	beginning_of_day = datetime(year=today.year, month=today.month, day=today.day, 
									hour=0, minute=0, second=0)
	return [EventTime(beginning_of_day + timedelta(hours=centroid.center), centroid.event_average()) \
			for centroid in centroids if centroid.is_valid()]


# event obj list for times and positions pulled by DB
def create_event_objects(results):
	return [EventTime(result[0], result[1]) for result in results]


# mathematical workhorse; creates centroids, does k-means & returns valid predicted events
def predict_events(events):
	initial_centroid_lists = initial_groups(events)
	centroids = k_means(events, initial_centroid_lists)
	predicted_events = create_new_events(centroids)  # centroids created; validate and set events

	return predicted_events



# —————————————————— OTHER ———————————————————

# sets events if all events that do not have surrounding events & not already passed
def set_events(cnx, cursor, curtain, events):
	for event in events:
		if not DBFunctions.event_set_at_approximate_time(cursor, curtain, event.datetime) \
		and event_is_not_past_current_time(event.datetime):
			DBFunctions.add_event(cnx, cursor, curtain, event.position, event.datetime)


# ————————————————— MAIN LOOP ——————————————————

# thread called by Master.py
def predictor_loop():
	while True:
		try:
			cnx, cursor = DBFunctions.connect_to_DB()
			for curtain in DBFunctions.curtain_ids(cursor):
				if DBFunctions.event_predictor(cursor, curtain):
					close_results = DBFunctions.close_events_for_day_for_last_four_weeks(cursor, curtain)
					close_event_times = create_event_objects(close_results)
					predicted_events = predict_events(close_event_times)
					set_events(cnx, cursor, curtain, predicted_events)

					open_results = DBFunctions.non_close_events_for_day_for_last_four_weeks(cursor, curtain)
					open_event_times = create_event_objects(open_results)
					predicted_events = predict_events(open_event_times)
					set_events(cnx, cursor, curtain, predicted_events)

			cnx.close()
			if current_time_is_past_sleep_point(): sleep_time = time_to_next_day()
			else: sleep_time = EVENT_PREDICTOR_SLEEP
			sleep(sleep_time)  # wait a day


		except Exception as error:
			try:
				import ErrorWriter
				ErrorWriter.write_error(error)
			except: pass
			sleep(ERROR_WAIT)



if __name__ == '__main__':
	predictor_loop()
