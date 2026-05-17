-- ============================================================
-- Migration: 008_donation.sql
-- Sprint 6 — DN-HS-01, DN-HS-02: Donee Donation History
-- ============================================================

CREATE TABLE IF NOT EXISTS donation (
    donation_id  INT            NOT NULL AUTO_INCREMENT,
    user_id      INT            NOT NULL,
    activity_id  INT            NOT NULL,
    amount       DECIMAL(10,2)  NOT NULL,
    donated_at   DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (donation_id),
    FOREIGN KEY (user_id)     REFERENCES useraccount(user_id)  ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activity(activity_id) ON DELETE CASCADE
);

-- ── Seed Data ─────────────────────────────────────────────────
-- donee01 (user_id=4) donations
INSERT INTO donation (user_id, activity_id, amount, donated_at) VALUES
(4, 1, 50.00,  '2026-03-01 10:00:00'),
(4, 2, 100.00, '2026-03-15 14:00:00'),
(4, 3, 75.00,  '2026-04-01 09:00:00'),
(4, 4, 200.00, '2026-04-10 11:00:00'),
(4, 5, 30.00,  '2026-05-01 08:00:00'),
(4, 1, 25.00,  '2026-05-10 16:00:00'),
(4, 3, 150.00, '2026-05-12 13:00:00');
