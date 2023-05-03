# `~/SmartCurtain/Hub/`

---

## Description
This folder is what goes on the Raspberry Pi (or other Hub devices).

### Contents
- `./DB/` The folder in which the SQL Schema & setup are held.
- `./Installation/` Where linux services & other setup files are held.
- `./Logs/` For log message files.
- `./Python/` The main scripts that are run as the server.
- `./Makefile` for install & uninstall

---


## Installation

### RASPBERRY PI
*This assumes the Raspberry Pi has already been connected to the internet, has Git and Docker*
- Clone repository to Raspberry Pi.
- Edit `~/SmartCurtain/Hub/DB/Sample.sql` as needed for your setup.
- Edit `~/SmartCurtain/Hub/Python/Other/Global.py` to supply your locale & information.
- `cd` into `~/SmartCurtain/Hub/`.
- Run `make` command.

Run 
```bash
make
```

## Update

Pulls the latest Production version and copies it to the working project directory.

Run
```bash
make update
```
