

import json


from SmartCurtain import Home


def test():
	homes = Home.all()
	home = homes[0]
	room = home[1]
	curtain = room[1]
	print(str(homes))
	print(str(room))
	print(str(curtain))


if(__name__ == "__main__"):
	test()
