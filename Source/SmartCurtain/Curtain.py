#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.19                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from typing import Dict, Optional
import warnings


import SmartCurtain
from Utility import warning_message, wrong_type_string


class Curtain(SmartCurtain.Area):
	def __init__(self, Room: Optional[SmartCurtain.Room]=None, *, id: int, is_deleted: bool, length: Optional[int],
		name: str, CurtainEvents: list[SmartCurtain.AreaEvent[SmartCurtain.Curtain]],
		CurtainOptions: list[SmartCurtain.AreaOption[SmartCurtain.Curtain]]
	):
		SmartCurtain.Area.__init__(self, id=id, is_deleted=is_deleted, name=name, AreaEvents=CurtainEvents,
			AreaOptions=CurtainOptions
		)
		# STRUCTURE #
		self.Room: SmartCurtain.Room = Room
		# DATABASE #
		self.length: Optional[int] = length
		# TEMP STATE #
		self.is_connected: bool = False
		self.is_moving: bool = False
		self.percentage: int = 0

		warnings.formatwarning = warning_message


	@staticmethod
	def from_dictionary(curtain_data: dict) -> SmartCurtain.Curtain:
		events: list[SmartCurtain.AreaEvent[SmartCurtain.Curtain]] = []
		for event_data in curtain_data["CurtainsEvents"]:
			event_data["Option"] = SmartCurtain.Option(**event_data["Option"]) if(event_data["Option"]) else None
			events.append(SmartCurtain.AreaEvent.from_dictionary[SmartCurtain.Curtain](event_data))

		options: list[SmartCurtain.AreaOption[SmartCurtain.Curtain]] = []
		for option_data in curtain_data["CurtainsOptions"]:
			option = SmartCurtain.Option(**option_data["Option"])
			options.append(SmartCurtain.AreaOption[SmartCurtain.Curtain](**{**option_data, "Option": option}))

		return Curtain(id=curtain_data["id"], is_deleted=curtain_data["is_deleted"], length=curtain_data["length"],
			name=curtain_data["name"], CurtainEvents=events, CurtainOptions=options
		)


	# —————————————————————————————————————————————— GETTERS & SETTERS  —————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

	def __getitem__(self, *_) -> None:
		raise NotImplementedError("Cannot use [int] operator as it has no child areas")


	def __iter__(self) -> dict:
		yield from {
			# DATABASE #
			"id": self._id,
			"is_deleted": self._is_deleted,
			"length": self._length,
			"name": self._name,
			"CurtainEvents": list(map(dict, self._CurtainEvents)),
			"CurtainOptions": list(map(dict, self._CurtainOptions)),
			# TEMP STATE #
			"is_connected": self._is_connected,
			"is_moving": self._is_moving,
			"percentage": self._percentage
		}.items()


	# ———————————————————————————————————————— GETTERS & SETTERS::ATTRIBUTES  ———————————————————————————————————————— #

	@property
	def is_moving(self) -> bool:
		return self._is_moving


	@is_moving.setter
	def is_moving(self, new_is_moving: bool) -> None:
		if(not isinstance(new_is_moving, bool)):
			raise TypeError(wrong_type_string(self, "is_moving", bool, new_is_moving))

		self._is_moving = new_is_moving


	@property
	def is_connected(self) -> bool:
		return self._is_connected


	@is_connected.setter
	def is_connected(self, new_is_connected: bool) -> None:
		if(not isinstance(new_is_connected, bool)):
			raise TypeError(wrong_type_string(self, "is_connecte", bool, new_is_connected))

		self._is_connected = new_is_connected


	@property
	def length(self) -> Optional[int]:
		return self._length


	@length.setter
	def length(self, new_length: Optional[int]) -> None:
		if(not isinstance(new_length, Optional[int])):
			raise TypeError(wrong_type_string(self, "length", Optional[int], new_length))

		self._length = new_length


	@property
	def percentage(self) -> int:
		return self._percentage


	@percentage.setter
	def percentage(self, new_percentage: int) -> None:
		if(not isinstance(new_percentage, int)):
			raise TypeError(wrong_type_string(self, "percentage", int, new_percentage))

		if(new_percentage < 0):
			warnings.warn(f"Percentage of '{new_percentage}' is being adjusted up to 0.")
			new_percentage = 0

		if(100 < new_percentage):
			warnings.warn(f"Percentage of '{new_percentage}' is being adjusted down to 100.")
			new_percentage = 0

		self._percentage = new_percentage


	def structure(self) -> Dict[str, SmartCurtain.Area]:
		return {
			"id": self._id,
			"Room.id": self._Room.id,
			"Home.id": self._Room.Home().id
		}


	# —————————————————————————————————————————— GETTERS & SETTERS::PARENTS —————————————————————————————————————————— #

	@property
	def Room(self) -> Optional[SmartCurtain.Room]:
		return self._Room


	@Room.setter
	def Room(self, new_Room: Optional[SmartCurtain.Room]=None) -> None:
		if(not isinstance(new_Room, Optional[SmartCurtain.Room])):
			raise TypeError(wrong_type_string(self, "Room", SmartCurtain.Room, new_Room))

		self._Room = new_Room
