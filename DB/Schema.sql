
-- 	Created by: MPZinke
-- 	on 2020.12.19
-- 
-- 	DESCRIPTION: Main DB script for creating Curtain DB.
-- 	BUGS:
-- 	FUTURE:


-- Primary table for curtain listing.
-- Details individual curtain setups.
DROP TABLE IF EXISTS "Curtains" CASCADE;
CREATE TABLE IF NOT EXISTS "Curtains"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"buffer_time" SMALLINT NOT NULL DEFAULT 0,  -- Curtain travel deci-seconds (prevent event overlap)
	CHECK("buffer_time" >= 0),
	"direction" BOOLEAN NOT NULL DEFAULT FALSE,
	"ip_address" VARCHAR(15) NOT NULL,
	"port" SMALLINT NOT NULL DEFAULT 80,
	CHECK("port" >= 0),
	"is_activated" BOOLEAN NOT NULL DEFAULT FALSE,
	"is_current" BOOLEAN NOT NULL DEFAULT TRUE,
	-- "is_safe": prevents actions from going to a percentage it thinks is harmful (EG opening farther while 'fully open')
	"is_safe" BOOLEAN NOT NULL DEFAULT TRUE,
	"is_smart" BOOLEAN NOT NULL DEFAULT TRUE,
	"last_connection" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"length" INT NOT NULL,
	CHECK("length" >= 0),
	"name" VARCHAR(32) NOT NULL UNIQUE,
	"percentage" SMALLINT NOT NULL DEFAULT 0,
	CHECK("percentage" >= 0)
);


DROP TABLE IF EXISTS "Options" CASCADE;
CREATE TABLE IF NOT EXISTS "Options"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"description" VARCHAR(256) NOT NULL DEFAULT '',
	"is_current" BOOLEAN NOT NULL DEFAULT TRUE,
	"name" VARCHAR(32) NOT NULL UNIQUE
);


DROP TABLE IF EXISTS "CurtainsOptions" CASCADE;
CREATE TABLE IF NOT EXISTS "CurtainsOptions"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Curtains.id" INT NOT NULL,
	CHECK("Curtains.id" >= 0),
	FOREIGN KEY ("Curtains.id") REFERENCES "Curtains"("id"),
	"Options.id" INT NOT NULL,
	CHECK("Options.id" >= 0),
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"data" TEXT NOT NULL DEFAULT '',
	"is_on" BOOLEAN NOT NULL,
	"notes" VARCHAR(256) DEFAULT NULL
);


DROP TABLE IF EXISTS "CurtainsEvents" CASCADE;
CREATE TABLE IF NOT EXISTS "CurtainsEvents"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Curtains.id" INT NOT NULL,
	CHECK("Curtains.id" >= 0),
	FOREIGN KEY ("Curtains.id") REFERENCES "Curtains"("id"),
	"Options.id" INT DEFAULT NULL,
	CHECK("Options.id" >= 0),
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"is_activated" BOOLEAN NOT NULL DEFAULT FALSE,
	"is_current" BOOLEAN NOT NULL DEFAULT TRUE,
	"percentage" INT NOT NULL,
	CHECK("percentage" >= 0),
	"time" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
