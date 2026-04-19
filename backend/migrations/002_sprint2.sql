-- ============================================================
-- Sprint 2 Migration
-- Database: csit314 (local) / railway (Railway)
-- Run: mysql -u root -p csit314 < migrations/002_sprint2.sql
-- ============================================================

-- Add phone column to useraccount
-- Needed for user profile management (UA-01 to UA-05)
ALTER TABLE `useraccount`
  ADD COLUMN `phone` VARCHAR(20) DEFAULT NULL AFTER `dob`;
