#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on ..                                                                                                              #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from typing import Dict


def compare_function_params(func1: Dict[str, type], func2: Dict[str, type]) -> Dict[str, type]:
	"""
	SUMMARY: Compares the args and types of two functions.
	PARAMS:  Takes the args and types of function 1 and the args and types of function 2.
	DETAILS: Iterates through the functions' parameters. Checks whether each of the parameters names and types matches.
	RETURNS: A dictionary of {<param_name>: [<function1_type>, <function2_type>]} for mismatched parameters.
	"""
	bad_function_params = {}
	for param in set(list(func1) + list(func2)):
		if(param != "return" and (param not in func1 or param not in func2 or func1[param] != func2[param])):
			bad_function_params[param] = [func[param] if(param in func) else None for func in [func1, func2]]

	return bad_function_params
