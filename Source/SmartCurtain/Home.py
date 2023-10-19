#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2023.04.07                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from bson.objectid import ObjectId
from typing import Dict, Optional


import SmartCurtain
from SmartCurtain import DB
from Utility import wrong_type_string, LookupStruct


class Home(SmartCurtain.Area):
	def __init__(self, *, _id: ObjectId, is_deleted: bool, name: str,
		HomeEvents: list[SmartCurtain.AreaEvent[SmartCurtain.Home]],
		HomeOptions: list[SmartCurtain.AreaOption[SmartCurtain.Home]], Rooms: list[SmartCurtain.Room]
	):
		SmartCurtain.Area.__init__(self, _id=_id, name=name, AreaEvents=HomeEvents, AreaOptions=HomeOptions)

		# STRUCTURE #
		self.Rooms: list[SmartCurtain.Room] = Rooms
		for room in self.Rooms:
			room.Home = self


	@staticmethod
	def all() -> list[SmartCurtain.Home]:
		options = SmartCurtain.Option.all()
		area_names = ["Homes", "Rooms", "Curtains"]
		areas_dicts = {area_name: DB.all_Areas(area_name) for area_name in area_names}
		areas_events_dicts = {area_name: DB.all_AreasEvents(f"{area_name}Events") for area_name in area_names}
		areas_options_dicts = {area_name: DB.all_AreasOptions(f"{area_name}Options") for area_name in area_names}

		for area_name, area_dicts in areas_dicts.items():
			for area_dict in area_dicts:
				filter_function = lambda item: item[f"{area_name}.id"]==area_dict["id"]
				# Associate AreaEvents & Options with AreaEvents.
				area_dict[f"{area_name}Events"] = list(filter(filter_function, areas_events_dicts[area_name]))
				for event_dict in area_dict[f"{area_name}Events"]:
					event_dict["Option"] = next(filter(lambda option: option==event_dict["Options.id"], options), None)
				# Associate AreaOptions & Options with AreaOptions.
				area_dict[f"{area_name}Options"] = list(filter(filter_function, areas_options_dicts[area_name]))
				for option_dict in area_dict[f"{area_name}Options"]:
					option_dict["Option"] = next(filter(lambda option: option==option_dict["Options.id"], options))

				# Associate Areas with Areas.
				if((child_area_names := {"Homes": "Rooms", "Rooms": "Curtains"}.get(area_name)) is not None):
					area_dict[child_area_names] = list(filter(filter_function, areas_dicts[child_area_names]))

		return [Home.from_dictionary(home_dict) for home_dict in areas_dicts["Homes"]]


	@staticmethod
	def current() -> list[SmartCurtain.Home]:
		options = SmartCurtain.Option.all()
		Homes = list(SmartCurtain.DB.SMART_CURTAIN_DATABASE.Homes.find())
		for Home in Homes:
			for area_option in Home["HomesOptions"]:
				area_option["Option"] = next(option for option in options if(option.id == area_option["Option"]))

			for Room in Home["Rooms"]:
				for area_option in Room["RoomsOptions"]:
					area_option["Option"] = next(option for option in options if(option.id == area_option["Option"]))

				for Curtain in Room["Curtains"]:
					for area_option in Curtain["CurtainsOptions"]:
						area_option["Option"] = next(option for option in options if(option.id == area_option["Option"]))

		return [SmartCurtain.Home.from_dictionary(home_dict) for home_dict in Homes]


	@staticmethod
	def from_dictionary(home_data: dict) -> SmartCurtain.Home:
		events: list[SmartCurtain.AreaEvent[SmartCurtain.Home]] = []
		for event_data in home_data["HomesEvents"]:
			events.append(SmartCurtain.AreaEvent.from_dictionary[SmartCurtain.Home](event_data))

		options: list[SmartCurtain.AreaOption[SmartCurtain.Home]] = []
		for option_data in home_data["HomesOptions"]:
			options.append(SmartCurtain.AreaOption.from_dictionary[SmartCurtain.Home](option_data))

		rooms: list[SmartCurtain.Room] = []
		for room_data in home_data["Rooms"]:
			rooms.append(SmartCurtain.Room.from_dictionary(room_data))

		return Home(id=home_data["id"], is_deleted=home_data["is_deleted"], name=home_data["name"], HomeEvents=events,
			HomeOptions=options, Rooms=rooms
		)


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __getitem__(self, Room_id: int|str) -> Optional[SmartCurtain.Room]|LookupStruct[SmartCurtain.Curtain]:
		"""
		RETURNS: If an int is supplied, the home with a matching ID is returned or none. If "-" is supplied, a
		         dictionary of the rooms and curtains is returned.
		         IE `{<curtain ids: curtains>}`
		"""
		return LookupStruct[SmartCurtain.Room, SmartCurtain.Curtain](self._Rooms)[Room_id]


	def __iter__(self) -> dict:
		yield from {
			"id": self._id,
			"is_deleted": self._is_deleted,
			"name": self._name,
			"HomeEvents": list(map(dict, self._HomeEvents)),
			"HomeOptions": list(map(dict, self._HomeOptions)),
			"Rooms": list(map(dict, self._Rooms))
		}.items()


	def structure(self) -> Dict[str, SmartCurtain.Area]:
		return {
			"id": self.id
		}


	# ————————————————————————————————————————— GETTERS & SETTERS::CHILDREN  ————————————————————————————————————————— #

	@property
	def Rooms(self) -> list[SmartCurtain.Room]:
		return self._Rooms.copy()


	@Rooms.setter
	def Rooms(self, new_Rooms: list[SmartCurtain.Room]) -> None:
		if(any(not isinstance(room, SmartCurtain.Room) for room in new_Rooms)):
			raise TypeError(wrong_type_string(self, "Rooms", list[SmartCurtain.Room], []))

		self._Rooms = new_Rooms.copy()


	@property
	def SmartCurtain(self) -> SmartCurtain.SmartCurtain:
		return self._SmartCurtain


	@SmartCurtain.setter
	def SmartCurtain(self, smart_curtain: Optional[object]) -> None:
		if(not isinstance(smart_curtain, SmartCurtain.SmartCurtain)):
			raise TypeError(wrong_type_string(self, "SmartCurtain", SmartCurtain.SmartCurtain, smart_curtain))

		self._SmartCurtain = smart_curtain
