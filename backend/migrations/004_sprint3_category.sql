-- ============================================================
-- Migration: 004_sprint3_category.sql
-- Sprint 3 — PM-01 to PM-05: FSA Category Management
-- ============================================================

CREATE TABLE IF NOT EXISTS category (
    category_id   INT          NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description   TEXT,
    status        VARCHAR(20)  NOT NULL DEFAULT 'active',
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (category_id)
);