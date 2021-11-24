

USE `SmartCurtain`;

-- Prepare for changes
SET `foreign_key_checks` = FALSE;
ALTER TABLE `CurtainsOptions` DROP INDEX `UNIQUE:CurtainsOptions`;

-- ———— Update Options.id's in CurtainsOptions ————
UPDATE `CurtainsOptions` SET `Options.id` = 1 WHERE `Options.id` = 2;  -- Combine Adafruit feeds into one
UPDATE `CurtainsOptions` SET `Options.id` = `Options.id` - 1  WHERE `Options.id` > 1;  -- Shift other columns down one

-- ———— Update Options.id's in Options ————
DELETE FROM `Options` WHERE `id` = 2;  -- Remove old Option
UPDATE `Options` SET `id` = `id` - 1;  -- Shift other columns down

-- Undo temporary preparations
SET `foreign_key_checks` = TRUE;
