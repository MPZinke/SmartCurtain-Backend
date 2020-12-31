# `~/SmartCurtain/Hub/Python/`

---

## DESCRIPTION
This folder holds the main scripts that are run as the server.

### CONTENTS
- `./Class/` Holds class objects used by Manager & Server subprocesses.
- `./DB/` Functions for accessing DB information.
- `./Manager/` The multi-threaded program that creates & manages future events.
- `./Other/` Other usefull tools, such as an Error logger
- `./Server/` The web interface for APIs & user interaction.
- `./System/` The main backend data structure that is a running state of the system and interfaces with the DB.
- `./SmartCurtain.py` The main program that is called by the Systemd service.
