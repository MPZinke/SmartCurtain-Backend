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
		return type(cls.__name__, (cls,), {"__args__": (__args__,)})


	@staticmethod
	def function(function: callable) -> object:
		return Generic(function)


	def __init__(self, function: callable):
		self._function = function


	def __call__(self, *args: list, **kwargs: dict):
		return self._function(self.__args__, *args, **kwargs)


	def __getitem__(self, __args__) -> callable:
		self.__args__ = __args__
		return self



@Generic.function
def my_function(__args__):
	print(__args__)


def test():
	print(my_function[str])
	my_function[str]()


if(__name__ == "__main__"):
	test()
