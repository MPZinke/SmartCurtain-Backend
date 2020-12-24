

from Python.DB.DBFunctions import __CONNECT__;
from Python.Class.Header import Header;


cnx, cursor = __CONNECT__("root", "mysql", "SmartCurtain");
header_test = Header(cursor);


def print_recurr(obj):
	if(isinstance(obj, (int, str, bool))):
		print(obj);
	elif(isinstance(obj, list)):
		for x in obj: print_recurr(x);
	else:
		for part in obj.__dict__: print_recurr(getattr(obj, part));


print_recurr(header_test);