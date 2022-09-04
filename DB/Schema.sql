
-- 	Created by: MPZinke
-- 	on 2020.12.19
-- 
-- 	DESCRIPTION: Main DB script for creating Curtain DB.
-- 	BUGS:
-- 	FUTURE:


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
	"Options.id" INT DEFAULT NULL,
	CHECK("Options.id" >= 0),
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"is_activated" BOOLEAN NOT NULL DEFAULT FALSE,
	"is_current" BOOLEAN NOT NULL DEFAULT TRUE,
	"percentage" INT NOT NULL,
	CHECK("percentage" >= 0),
	"time" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
