#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2023.04.08                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


class Generic:
	def __class_getitem__(cls, __args__):
		if(not isinstance(__args__, tuple)):
			__args__ = (__args__,)

		return type(cls.__name__, (cls,), {"__args__": __args__})


	# ———— WRAPPER ———— #

	def __init__(self, function: callable):
		self._function = function


	def __call__(self, *args: list, **kwargs: dict):
		return self._function(self.__args__, *args, **kwargs)


	def __getitem__(self, __args__) -> callable:
		if(not isinstance(__args__, tuple)):
			__args__ = (__args__,)

		self.__args__ = __args__
		return self



@Generic
def my_function(__args__, *args, **kwargs):
	print(f"my_function[{__args__[0].__name__}]")
	print(args, kwargs)


def test():
	print(my_function[str, int])
	my_function[str](1, 2, key="word")


if(__name__ == "__main__"):
	test()
