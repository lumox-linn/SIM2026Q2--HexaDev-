from flask import Blueprint, jsonify
from app import mysql

setup_bp = Blueprint('setup', __name__)


@setup_bp.route('/setup', methods=['GET'])
def setup():
    """
    Temporary endpoint to create tables and seed demo accounts.
    Visit: https://your-backend.railway.app/setup
    DELETE THIS FILE after running once!
    """
    try:
        cursor = mysql.connection.cursor()

        # Create useraccount table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `useraccount` (
              `user_id`         INT(8)       NOT NULL AUTO_INCREMENT,
              `username`        VARCHAR(50)  NOT NULL,
              `password_hash`   VARCHAR(255) NOT NULL,
              `isActive`        TINYINT(1)   NOT NULL DEFAULT 1,
              `role`            ENUM('admin','fund_raiser','donee','platform_manager') NOT NULL,
              `created_at`      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
              `profile_picture` VARCHAR(255) DEFAULT NULL,
              PRIMARY KEY (`user_id`),
              UNIQUE KEY `username` (`username`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Create usersession table
        cursor.execute("""
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        mysql.connection.commit()

        # Seed demo accounts
        from werkzeug.security import generate_password_hash

        users = [
            ('admin01',     generate_password_hash('admin123'),   1, 'admin'),
            ('fr01',        generate_password_hash('fr123'),      1, 'fund_raiser'),
            ('donee01',     generate_password_hash('donee123'),   1, 'donee'),
            ('pm01',        generate_password_hash('pm123'),      1, 'platform_manager'),
            ('suspended01', generate_password_hash('test123'),    0, 'donee'),
        ]

        cursor.executemany(
            "INSERT IGNORE INTO useraccount (username, password_hash, isActive, role) VALUES (%s, %s, %s, %s)",
            users
        )
        mysql.connection.commit()
        seeded = cursor.rowcount
        cursor.close()

        return jsonify({
            'status':  'success',
            'message': f'Tables created and {seeded} demo accounts seeded!',
            'accounts': [
                {'username': 'admin01',     'password': 'admin123',  'role': 'admin'},
                {'username': 'fr01',        'password': 'fr123',     'role': 'fund_raiser'},
                {'username': 'donee01',     'password': 'donee123',  'role': 'donee'},
                {'username': 'pm01',        'password': 'pm123',     'role': 'platform_manager'},
                {'username': 'suspended01', 'password': 'test123',   'role': 'donee (suspended)'},
            ]
        }), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500