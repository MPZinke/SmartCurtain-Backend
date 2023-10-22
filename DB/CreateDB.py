

from bson.objectid import ObjectId
import json
import os
from pymongo import MongoClient
from typing import Dict


def create_collections_with_validation(smart_curtain_database) -> None:
	smart_curtain_database.drop_collection("Options")
	smart_curtain_database.create_collection("Options")
	with open(f"./Validation/Options.json", "r") as file:
		smart_curtain_database.command("collMod", "Options", validator=json.load(file))

	for collection_name in ["Curtains", "Rooms", "Homes"]:
		smart_curtain_database.drop_collection(collection_name)
		smart_curtain_database.create_collection(collection_name)
		with open(f"./Validation/{collection_name}.json", "r") as file:
			smart_curtain_database.command("collMod", collection_name, validator=json.load(file))

		smart_curtain_database.drop_collection(f"{collection_name}Events")
		smart_curtain_database.create_collection(f"{collection_name}Events")
		with open(f"./Validation/{collection_name}Events.json", "r") as file:
			smart_curtain_database.command("collMod", f"{collection_name}Events", validator=json.load(file))


def insert_Curtain(smart_curtain_database, Options_ids: Dict[int, ObjectId], Curtain: dict) -> None:
	CurtainsEvents_ids = []
	for CurtainsEvent in Curtain["CurtainsEvents"]:
		database_CurtainsEvent = {key: value for key, value in CurtainsEvent.items() if(key != "id")}
		database_CurtainsEvent.update({"Options": next((Options_ids[id] for id in Options_ids if(id == CurtainsEvent["id"])), None)})
		CurtainsEvents_ids.append(smart_curtain_database.CurtainsEvents.insert_one(database_CurtainsEvent).inserted_id)

	CurtainsOptions_ids = []
	for CurtainsOption in Curtain["CurtainsOptions"]:
		database_CurtainsOption = {key: value for key, value in CurtainsOption.items() if(key != "id")}
		database_CurtainsOption.update({"Option": next(Options_ids[id] for id in Options_ids if(id == CurtainsOption["id"]))})
		CurtainsOptions_ids.append(database_CurtainsOption)

	database_Curtain = {key: value for key, value in Curtain.items() if(key != "id")}
	database_Curtain.update({"CurtainsEvents": CurtainsEvents_ids, "CurtainsOptions": CurtainsOptions_ids})
	return smart_curtain_database.Curtains.insert_one(database_Curtain).inserted_id


def insert_Room(smart_curtain_database, Options_ids: Dict[int, ObjectId], Room: dict) -> None:
	RoomsEvents_ids = []
	for RoomsEvent in Room["RoomsEvents"]:
		database_RoomsEvent = {key: value for key, value in RoomsEvent.items() if(key != "id")}
		database_RoomsEvent.update({"Options": next((Options_ids[id] for id in Options_ids if(id == RoomsEvent["id"])), None)})
		RoomsEvents_ids.append(smart_curtain_database.RoomsEvents.insert_one(database_RoomsEvent).inserted_id)

	RoomsOptions_ids = []
	for RoomsOption in Room["RoomsOptions"]:
		database_RoomsOption = {key: value for key, value in RoomsOption.items() if(key != "id")}
		database_RoomsOption.update({"Option": next(Options_ids[id] for id in Options_ids if(id == RoomsOption["id"]))})
		RoomsOptions_ids.append(database_RoomsOption)

	Curtains_ids = []
	for Curtain in Room["Curtains"]:
		Curtains_ids.append(insert_Curtain(smart_curtain_database, Options_ids, Curtain))

	database_Room = {key: value for key, value in Room.items() if(key != "id")}
	database_Room.update({"RoomsEvents": RoomsEvents_ids, "RoomsOptions": RoomsOptions_ids, "Curtains": Curtains_ids})
	return smart_curtain_database.Rooms.insert_one(database_Room).inserted_id


def insert_Home(smart_curtain_database, Options_ids: Dict[int, ObjectId], Home: dict) -> None:
	HomesEvents_ids = []
	for HomesEvent in Home["HomesEvents"]:
		database_HomesEvent = {key: value for key, value in HomesEvent.items() if(key != "id")}
		database_HomesEvent.update({"Options": next((Options_ids[id] for id in Options_ids if(id == HomesEvent["id"])), None)})
		HomesEvents_ids.append(smart_curtain_database.HomesEvents.insert_one(database_HomesEvent).inserted_id)

	HomesOptions_ids = []
	for HomesOption in Home["HomesOptions"]:
		database_HomesOption = {key: value for key, value in HomesOption.items() if(key != "id")}
		database_HomesOption.update({"Option": next(Options_ids[id] for id in Options_ids if(id == HomesOption["id"]))})
		HomesOptions_ids.append(database_HomesOption)

	Rooms_ids = []
	for Room in Home["Rooms"]:
		Rooms_ids.append(insert_Room(smart_curtain_database, Options_ids, Room))

	database_Home = {key: value for key, value in Home.items() if(key != "id")}
	database_Home.update({"HomesEvents": HomesEvents_ids, "HomesOptions": HomesOptions_ids, "Rooms": Rooms_ids})
	return smart_curtain_database.Homes.insert_one(database_Home).inserted_id



def add_data(smart_curtain_database) -> None:
	with open("Data/Options.json", "r") as file:
		Options = json.load(file)

	Options_ids = {}
	for Option in Options:
		database_Option = {key: value for key, value in Option.items() if(key != "id")}
		Options_ids[Option["id"]] = smart_curtain_database.Options.insert_one(database_Option).inserted_id

	with open("Data/Homes.json", "r") as file:
		Homes = json.load(file)

	for Home in Homes:
		insert_Home(smart_curtain_database, Options_ids, Home)


def main():
	host = os.getenv("MONGO_HOST")
	user = os.getenv("MONGO_USER")
	password = os.getenv("MONGO_PASSWORD")
	connection_string = f"""mongodb://{user}:{password}@{host}/SmartCurtain"""

	client = MongoClient(connection_string)
	smart_curtain_database = client.SmartCurtain

	create_collections_with_validation(smart_curtain_database)
	add_data(smart_curtain_database)


if(__name__ == "__main__"):
	main()
