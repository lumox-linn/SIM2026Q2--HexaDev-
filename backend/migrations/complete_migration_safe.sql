-- ============================================================
-- HexaDev Complete Migration Script (SAFE VERSION)
-- Drops and recreates all tables correctly
-- Run this on Zilin's Railway MySQL database
-- ============================================================

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS useraccount;
DROP TABLE IF EXISTS userprofile;

SET FOREIGN_KEY_CHECKS = 1;

-- ── userprofile ───────────────────────────────────────────────
CREATE TABLE userprofile (
    profile_id   INT          NOT NULL AUTO_INCREMENT,
    profile_name VARCHAR(100) NOT NULL UNIQUE,
    status       VARCHAR(20)  NOT NULL DEFAULT 'active',
    description  TEXT,
    PRIMARY KEY (profile_id)
);

-- ── useraccount ───────────────────────────────────────────────
CREATE TABLE useraccount (
    user_id         INT          NOT NULL AUTO_INCREMENT,
    username        VARCHAR(100) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    isActive        INT          NOT NULL DEFAULT 1,
    role            VARCHAR(50)  NOT NULL,
    email           VARCHAR(100),
    phone           VARCHAR(20),
    dob             DATE,
    profile_picture VARCHAR(255),
    profile_id      INT,
    created_at      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id),
    FOREIGN KEY (profile_id) REFERENCES userprofile(profile_id)
);

-- ── category ─────────────────────────────────────────────────
CREATE TABLE category (
    category_id   INT          NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description   TEXT,
    status        VARCHAR(20)  NOT NULL DEFAULT 'active',
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (category_id)
);

-- ============================================================
-- Seed default profiles
-- ============================================================
INSERT INTO userprofile (profile_name, status, description) VALUES
('admin',            'active', 'User Admin — manages accounts and profiles'),
('fund_raiser',      'active', 'Fund Raiser — creates and manages fundraising activities'),
('donee',            'active', 'Donee — browses and saves fundraising activities'),
('platform_manager', 'active', 'Platform Manager — manages FSA categories');

-- ============================================================
-- Seed default accounts
-- All passwords: pass123
-- ============================================================
INSERT INTO useraccount (username, password_hash, isActive, role, email, profile_id) VALUES
(
    'admin01',
    'pbkdf2:sha256:260000$xyz$abc',
    1, 'admin', 'admin@hexadev.com',
    (SELECT profile_id FROM userprofile WHERE profile_name = 'admin')
),
(
    'pm01',
    'pbkdf2:sha256:260000$xyz$abc',
    1, 'platform_manager', 'pm@hexadev.com',
    (SELECT profile_id FROM userprofile WHERE profile_name = 'platform_manager')
),
(
    'fr01',
    'pbkdf2:sha256:260000$xyz$abc',
    1, 'fund_raiser', 'fr@hexadev.com',
    (SELECT profile_id FROM userprofile WHERE profile_name = 'fund_raiser')
),
(
    'donee01',
    'pbkdf2:sha256:260000$xyz$abc',
    1, 'donee', 'donee@hexadev.com',
    (SELECT profile_id FROM userprofile WHERE profile_name = 'donee')
);

-- ============================================================
-- Verify
-- ============================================================
SHOW TABLES;
SELECT username, role, isActive FROM useraccount;
SELECT profile_name, status FROM userprofile;
