-- ============================================================
-- Migration: 005_sprint4_activity.sql
-- Sprint 4 — FR-01 to FR-05: Fundraising Activity Management
-- ============================================================

CREATE TABLE IF NOT EXISTS activity (
    activity_id   INT            NOT NULL AUTO_INCREMENT,
    title         VARCHAR(200)   NOT NULL,
    description   TEXT,
    category_id   INT            DEFAULT NULL,
    created_by    INT            NOT NULL,
    target_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    amount_raised DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    start_date    DATE,
    end_date      DATE,
    status        VARCHAR(20)    NOT NULL DEFAULT 'active',
    created_at    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (activity_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE SET NULL,
    FOREIGN KEY (created_by)  REFERENCES useraccount(user_id)  ON DELETE CASCADE
);
