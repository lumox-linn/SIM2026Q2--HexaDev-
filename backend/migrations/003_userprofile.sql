-- ============================================================
-- Sprint 2 Migration — User Profile Table
-- Run on Aiven after 002_sprint2.sql
-- ============================================================

-- Step 1: Create userprofile table
CREATE TABLE IF NOT EXISTS `userprofile` (
  `profile_id`   INT(8)       NOT NULL AUTO_INCREMENT,
  `profile_name` VARCHAR(50)  NOT NULL,
  `status`       ENUM('active','suspended') NOT NULL DEFAULT 'active',
  `description`  VARCHAR(255) DEFAULT NULL,
  `created_at`   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`profile_id`),
  UNIQUE KEY `profile_name` (`profile_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Step 2: Insert the 4 default profiles
INSERT IGNORE INTO `userprofile` (profile_name, status, description) VALUES
('admin',            'active', 'System administrator — manages user accounts and profiles'),
('fund_raiser',      'active', 'Fund Raiser — creates and manages fundraising campaigns'),
('donee',            'active', 'Donee — browses and saves fundraising activities'),
('platform_manager', 'active', 'Platform Manager — manages categories and generates reports');

-- Step 3: Add profile_id column to useraccount
ALTER TABLE `useraccount`
  ADD COLUMN `profile_id` INT(8) DEFAULT NULL AFTER `role`;

-- Step 4: Set profile_id based on existing role values
UPDATE `useraccount` ua
JOIN `userprofile` up ON ua.role = up.profile_name
SET ua.profile_id = up.profile_id;

-- Step 5: Add Foreign Key constraint
ALTER TABLE `useraccount`
  ADD CONSTRAINT `fk_account_profile`
  FOREIGN KEY (`profile_id`) REFERENCES `userprofile` (`profile_id`)
  ON UPDATE CASCADE;
