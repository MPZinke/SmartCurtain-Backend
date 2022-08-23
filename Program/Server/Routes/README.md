# `~/SmartCurtain/Hub/Python/Server/Routes/`

---

## DESCRIPTION
Main routes python request handlers.

### CONTENTS
- `./Activate.py` Requests for moving curtain to certain positions.
- `./Root.py` Requests from URL root, including primary pages.
- `./State.py` Requests for information about curtain.


## Endpoints

### Root

`GET /`—Main page create new current event.

`GET /edit`–Page to edit upcoming events.

`GET /events`—Page to display the current events.

`GET /new`—Page to create new event.

`GET /favicon`—Garbage :)


### API

`GET /api`—Lists the available API versions.

`GET /api/v1.0`—The current version of this API.

`GET /api/v1.0/curtains`—Lists options available related to Curtains.

`GET /api/v1.0/curtains/all`—Lists all curtains.

`POST /api/v1.0/curtains/new`—Creates a new curtain with the JSON body.

`GET /api/v1.0/curtain/<string:curtain_name|int:curtain_id>`—Show information for a curtain.

`PATCH /api/v1.0/curtain/<string:curtain_name|int:curtain_id>`—Updates curtain's value(s) based on JSON body.

`GET /api/v1.0/curtain/<string:curtain_name|int:curtain_id>/events`—Lists all events for a curtain.

`GET /api/v1.0/curtain/<string:curtain_name|int:curtain_id>/event/<string:time|int:event_id>`—Show information for an event for a curtain.

`PATCH /api/v1.0/curtain/<string:curtain_name|int:curtain_id>/event/<string:time|int:event_id>`—Updates curtain's events' value(s) based on JSON body.

`GET /api/v1.0/events`—Lists options available related to Events.

`GET /api/v1.0/events/all`—Lists all events.

`GET /api/v1.0/event/<int:event_id>`—Show information for an event.

`POST /api/v1.0/event/new`—Creates a new event with the JSON body.

`GET /api/v1.0/options`—Lists all options available related to Options.

`GET /api/v1.0/options/all`—Lists all options.

`GET /api/v1.0/option/<int:option_id>`—Show information for a curtain.
