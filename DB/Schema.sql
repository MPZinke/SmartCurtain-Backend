
-- 	Created by: MPZinke
-- 	on 2020.12.19
-- 
-- 	DESCRIPTION: Main DB script for creating Curtain DB.
-- 	BUGS:
-- 	FUTURE:


CREATE EXTENSION btree_gist;


DROP TABLE IF EXISTS "Options" CASCADE;
CREATE TABLE IF NOT EXISTS "Options"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"description" VARCHAR(256) NOT NULL DEFAULT '',
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"name" VARCHAR(32) NOT NULL UNIQUE
);


DROP TABLE IF EXISTS "Homes" CASCADE;
CREATE TABLE IF NOT EXISTS "Homes"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"name" VARCHAR(32) NOT NULL
);


CREATE UNIQUE INDEX ON "Homes"("name")
  WHERE "is_deleted" = FALSE;


DROP TABLE IF EXISTS "HomesOptions" CASCADE;
CREATE TABLE IF NOT EXISTS "HomesOptions"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Homes.id" INT NOT NULL,
	FOREIGN KEY ("Homes.id") REFERENCES "Homes"("id"),
	"Options.id" INT NOT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"data" JSON DEFAULT NULL,
	"is_on" BOOLEAN NOT NULL,
	"notes" VARCHAR(256) NOT NULL DEFAULT '',
	UNIQUE ("Homes.id", "Options.id")
);


DROP TABLE IF EXISTS "Rooms" CASCADE;
CREATE TABLE IF NOT EXISTS "Rooms"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"name" VARCHAR(32) NOT NULL,
	"Homes.id" INT NOT NULL,
	FOREIGN KEY ("Homes.id") REFERENCES "Homes"("id")
);


CREATE UNIQUE INDEX ON "Rooms"("Homes.id", REGEXP_REPLACE("name", '[^_\-a-zA-Z0-9]', ''))
  WHERE "is_deleted" = FALSE;


DROP TABLE IF EXISTS "RoomsOptions" CASCADE;
CREATE TABLE IF NOT EXISTS "RoomsOptions"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Rooms.id" INT NOT NULL,
	FOREIGN KEY ("Rooms.id") REFERENCES "Rooms"("id"),
	"Options.id" INT NOT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"data" JSON DEFAULT NULL,
	"is_on" BOOLEAN NOT NULL,
	"notes" VARCHAR(256) NOT NULL DEFAULT '',
	UNIQUE ("Rooms.id", "Options.id")
);


DROP TABLE IF EXISTS "Curtains" CASCADE;
CREATE TABLE IF NOT EXISTS "Curtains"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"buffer_time" INT NOT NULL DEFAULT 0,  -- seconds
	"direction" BOOLEAN DEFAULT NULL,  -- NULL if curtain should use hardcoded values otherwise valued
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"length" INT DEFAULT NULL,  -- NULL if curtain should use hardcoded values otherwise valued
	CHECK("length" > 0 OR "length" IS NULL),
	"name" VARCHAR(32) NOT NULL,
	"Rooms.id" INT NOT NULL,
	FOREIGN KEY ("Rooms.id") REFERENCES "Rooms"("id")
);


CREATE UNIQUE INDEX ON "Curtains"("Rooms.id", REGEXP_REPLACE("name", '[^_\-a-zA-Z0-9]', ''))
  WHERE "is_deleted" = FALSE;


DROP TABLE IF EXISTS "CurtainsOptions" CASCADE;
CREATE TABLE IF NOT EXISTS "CurtainsOptions"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Curtains.id" INT NOT NULL,
	FOREIGN KEY ("Curtains.id") REFERENCES "Curtains"("id"),
	"Options.id" INT NOT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"data" JSON DEFAULT NULL,
	"is_on" BOOLEAN NOT NULL,
	"notes" VARCHAR(256) NOT NULL DEFAULT '',
	UNIQUE ("Curtains.id", "Options.id")
);


DROP TABLE IF EXISTS "CurtainsEvents" CASCADE;
CREATE TABLE IF NOT EXISTS "CurtainsEvents"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Curtains.id" INT NOT NULL,
	FOREIGN KEY ("Curtains.id") REFERENCES "Curtains"("id"),
	"Options.id" INT DEFAULT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"is_activated" BOOLEAN NOT NULL DEFAULT FALSE,
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"percentage" INT NOT NULL,
	CHECK("percentage" >= 0),
	"time" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	EXCLUDE USING GIST
	(
		"Curtains.id" WITH =, 
		TSRANGE("time" - INTERVAL '2 SECONDS', "time" + INTERVAL '2 SECONDS') WITH &&
    )
    WHERE ("is_deleted" = FALSE)
);


CREATE UNIQUE INDEX ON "CurtainsEvents"("Curtains.id", "time")
  WHERE "is_deleted" = FALSE;


DROP FUNCTION IF EXISTS update_old_CurtainsEvents() CASCADE;
CREATE FUNCTION update_old_CurtainsEvents() RETURNS TRIGGER AS $$
BEGIN
	UPDATE "CurtainsEvents" SET "is_deleted" = TRUE WHERE "time" < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


-- DROP TRIGGER IF EXISTS "DeleteOldCurtainEvents" ON "CurtainsEvents";
-- CREATE TRIGGER "DeleteOldCurtainEvents"
--   BEFORE SELECT ON "CurtainsEvents"
--   FOR EACH ROW
--   EXECUTE PROCEDURE update_old_CurtainsEvents();


-- ———————————————————————————————————————————————— DELETE INTEGRITY ———————————————————————————————————————————————— --

DROP FUNCTION IF EXISTS update_Homes_deletion() CASCADE;
CREATE FUNCTION update_Homes_deletion() RETURNS TRIGGER AS $$
BEGIN
	UPDATE "Rooms" SET "is_deleted" = TRUE WHERE "Homes.id" = NEW."id";
	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


-- Delete CurtainsEvents & CurtainsOptions when Curtain is deleted.
DROP TRIGGER IF EXISTS "DeleteHomesTrigger" ON "Homes";
CREATE TRIGGER "DeleteHomesTrigger"
  AFTER UPDATE ON "Homes"
  FOR EACH ROW
  WHEN (NEW."is_deleted" = TRUE)
  EXECUTE PROCEDURE update_Homes_deletion();


DROP FUNCTION IF EXISTS update_Rooms_deletion() CASCADE;
CREATE FUNCTION update_Rooms_deletion() RETURNS TRIGGER AS $$
BEGIN
	UPDATE "Curtains" SET "is_deleted" = TRUE WHERE "Rooms.id" = NEW."id";
	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


-- Delete CurtainsEvents & CurtainsOptions when Curtain is deleted.
DROP TRIGGER IF EXISTS "DeleteRoomsTrigger" ON "Rooms";
CREATE TRIGGER "DeleteRoomsTrigger"
  AFTER UPDATE ON "Rooms"
  FOR EACH ROW
  WHEN (NEW."is_deleted" = TRUE)
  EXECUTE PROCEDURE update_Rooms_deletion();



DROP FUNCTION IF EXISTS update_Curtains_deletion() CASCADE;
CREATE FUNCTION update_Curtains_deletion() RETURNS TRIGGER AS $$
BEGIN
	UPDATE "CurtainsEvents" SET "is_deleted" = TRUE WHERE "Curtains.id" = NEW."id";
	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


-- Delete CurtainsEvents & CurtainsOptions when Curtain is deleted.
DROP TRIGGER IF EXISTS "DeleteCurtainsTrigger" ON "Curtains";
CREATE TRIGGER "DeleteCurtainsTrigger"
  AFTER UPDATE ON "Curtains"
  FOR EACH ROW
  WHEN (NEW."is_deleted" = TRUE)
  EXECUTE PROCEDURE update_Curtains_deletion();
