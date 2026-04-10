-- ============================================================
-- Sprint 1 Migration
-- Database: csit314
-- Tables: useraccount, usersession
-- Run: mysql -u root -p < migrations/001_create_tables.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS csit314;
USE csit314;

-- ── useraccount ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `useraccount` (
  `user_id`       INT(8)       NOT NULL AUTO_INCREMENT,
  `username`      VARCHAR(50)  NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `isActive`      TINYINT(1)   NOT NULL DEFAULT 1,
  `role`          ENUM('admin','fund_raiser','donee','platform_manager') NOT NULL,
  `created_at`    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ── usersession ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `usersession` (
  `session_id`  INT(8)      NOT NULL AUTO_INCREMENT,
  `user_id`     INT(8)      NOT NULL,
  `token`       VARCHAR(64) NOT NULL,
  `login_time`  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `logout_time` DATETIME    DEFAULT NULL,
  `expires_at`  DATETIME    NOT NULL,
  `status`      ENUM('active','expired') NOT NULL DEFAULT 'active',
  PRIMARY KEY (`session_id`),
  UNIQUE KEY `token` (`token`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `fk_session_user`
    FOREIGN KEY (`user_id`) REFERENCES `useraccount` (`user_id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
