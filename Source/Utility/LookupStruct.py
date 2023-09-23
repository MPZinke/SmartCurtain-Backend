

from mpzinke import Generic


class LookupStruct(Generic):
	"""
	Dict[Home, Room, Curtain]
	"""
	def __init__(self, values: list[Generic]):
		self._values: list[Generic] = values


	def __getitem__(self, key: int|str):
		if(len(self.__args__) == 1 and key == "-"):
			raise Exception(f"Cannot further recurse Dict[{self.__args__[0].__name__}]")

		if(key != "-"):
			return next((value for value in self._values if(value.id() == key)), None)

		# EG. [room for home in self._homes for room in home.Rooms()]
		subvalues = []
		for value in self._values:
			subvalues += [subvalue for subvalue in getattr(value, f"{self.__args__[1].__name__}s")()]
		return LookupStruct[self.__args__[1:]](subvalues)


	def __iter__(self) -> list[Generic]:
		yield from self._values


	def __str__(self):
		return f"""Dict[{", ".join([arg.__name__ for arg in self.__args__])}]: {[str(value) for value in self._values]}"""
