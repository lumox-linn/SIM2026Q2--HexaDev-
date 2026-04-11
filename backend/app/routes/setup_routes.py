from flask import Blueprint, jsonify
import os

setup_bp = Blueprint('setup', __name__)


@setup_bp.route('/setup', methods=['GET'])
def setup():
    """Temporary endpoint — DELETE after running once!"""
    try:
        import pymysql
        from werkzeug.security import generate_password_hash

        conn = pymysql.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DB', 'railway'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
        )
        cursor = conn.cursor()

        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `useraccount` (
              `user_id`         INT(8)       NOT NULL AUTO_INCREMENT,
              `username`        VARCHAR(50)  NOT NULL,
              `password_hash`   VARCHAR(255) NOT NULL,
              `isActive`        TINYINT(1)   NOT NULL DEFAULT 1,
              `role`            ENUM('admin','fund_raiser','donee','platform_manager') NOT NULL,
              `created_at`      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
              `profile_picture` VARCHAR(255) DEFAULT NULL,
              `email`           VARCHAR(100) DEFAULT NULL,
              `dob`             DATE         DEFAULT NULL,
              PRIMARY KEY (`user_id`),
              UNIQUE KEY `username` (`username`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

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

        # Add email and dob columns if they don't exist
        try:
            cursor.execute("ALTER TABLE `useraccount` ADD COLUMN `email` VARCHAR(100) DEFAULT NULL")
        except Exception:
            pass  # Column already exists

        try:
            cursor.execute("ALTER TABLE `useraccount` ADD COLUMN `dob` DATE DEFAULT NULL")
        except Exception:
            pass  # Column already exists

        conn.commit()

        # Seed accounts
        users = [
            ('admin01',     generate_password_hash('admin123'),   1, 'admin'),
            ('fr01',        generate_password_hash('fr123'),      1, 'fund_raiser'),
            ('donee01',     generate_password_hash('donee123'),   1, 'donee'),
            ('pm01',        generate_password_hash('pm123'),      1, 'platform_manager'),
            ('suspended01', generate_password_hash('test123'),    0, 'donee'),
        ]

        inserted = 0
        for user in users:
            try:
                cursor.execute(
                    "INSERT IGNORE INTO useraccount (username, password_hash, isActive, role) VALUES (%s, %s, %s, %s)",
                    user
                )
                inserted += cursor.rowcount
            except Exception:
                pass

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'status':  'success',
            'message': f'Tables ready! email and dob columns added. {inserted} accounts seeded.',
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