

import mpzinke
import os
import pathlib


import Routes


FRONTEND_DIRECTORY = str(pathlib.Path(__file__).parent)
TEMPLATE_DIRECTORY = os.path.join(FRONTEND_DIRECTORY, "HTML", "Root")
STATIC_DIRECTORY = os.path.join(FRONTEND_DIRECTORY, "HTML", "Static")


def main():
	server = mpzinke.Server(name="SmartCurtain-Frontend",
		template_folder=TEMPLATE_DIRECTORY, static_folder=STATIC_DIRECTORY
	)

	server._app.add_url_rule("/", "/", Routes.Root.index, ["GET"])

	server(port=80)


if(__name__ == "__main__"):
	main()
