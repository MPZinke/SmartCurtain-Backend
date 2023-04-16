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


	def staticmethod(function: callable) -> object:
		return Generic(function)


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


def test():
	class Test(Generic):
		def __init__(self, a, b):
			print(f"Test[{self.__args__[0].__name__}]{a, b}")


		def my_method(self, a, b):
			print(f"""called `Test[{self.__args__[0].__name__}]::my_method({a}, {b})`""")


		@Generic
		def my_staticmethod(__args__, a, b):
			print(f"""called `Test::my_staticmethod[{__args__[0].__name__}]({a}, {b})`""")


	test = Test[int](1, 2)
	test.my_method(1, 2)
	Test.my_staticmethod[int](1, 2)


	@Generic
	def my_function(__args__, *args, **kwargs):
		args_string = ", ".join([str(arg) for arg in args])
		kwargs_string = ",".join([f"{key}={value}" for key, value in kwargs.items()])
		print(f"""called `my_function[{__args__[0].__name__}]({args_string}, {kwargs_string})`""")


	my_function[str]("a", "b", key="word")


if(__name__ == "__main__"):
	test()
