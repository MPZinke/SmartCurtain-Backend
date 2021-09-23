# `~/SmartCurtain/Hub/`

---

## DESCRIPTION
This folder is what goes on the Raspberry Pi (or other Hub devices).

### CONTENTS
- `./DB/` The folder in which the SQL Schema & setup are held.
- `./Installation/` Where linux services & other setup files are held.
- `./Logs/` For log message files.
- `./Python/` The main scripts that are run as the server.
- `./Makefile` for install & uninstall

---


## INSTALL

Run 
```bash
make
```

## UPDATE

Pulls the latest Production version and copies it to the working project directory.

Run
```bash
make update
```
