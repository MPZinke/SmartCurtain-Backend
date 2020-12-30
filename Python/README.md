# `~/SmartCurtain/Hub/Python/`

---

## DESCRIPTION
This folder holds the main scripts that are run as the server.

### CONTENTS
- `./SmartCurtain.py` The main program that is called by the Systemd service.
- `./Manager/` The multi-threaded program that creates & manages future events.
- `./Server/` The web interface for APIs & user interaction.
- `./System/` The main backend data structure that is a running state of the system and interfaces with the DB.

As dependencies to this, this folder also contains:
- `./Class/` Holds class objects used by Manager & Server subprocesses.
- `./DB/` Functions for accessing DB information.
- `./Other/` Other usefull tools, such as an Error logger
