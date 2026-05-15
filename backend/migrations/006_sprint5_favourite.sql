-- ============================================================
-- Migration: 006_sprint5_favourite.sql
-- Sprint 5 — DN-03 to DN-05: Donee Favourites
-- ============================================================

CREATE TABLE IF NOT EXISTS favourite (
    favourite_id INT      NOT NULL AUTO_INCREMENT,
    user_id      INT      NOT NULL,
    activity_id  INT      NOT NULL,
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (favourite_id),
    UNIQUE KEY unique_fav (user_id, activity_id),
    FOREIGN KEY (user_id)     REFERENCES useraccount(user_id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activity(activity_id) ON DELETE CASCADE
);
