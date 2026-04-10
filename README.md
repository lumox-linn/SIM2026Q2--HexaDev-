# Fundraising System — CSIT314 Group Project

## Stack
- **Frontend**: React + Vite (port 5173)
- **Backend**: Python Flask REST API (port 5000)
- **Database**: MySQL — database name `csit314`
- **Testing**: Pytest (backend)
- **CI/CD**: GitHub Actions

## Project structure
```
fundraising-system/
├── frontend/                   # React app (Yimin)
├── backend/                    # Flask API (Sylvia + Zilin)
│   ├── app/
│   │   ├── models/
│   │   │   ├── user_account.py     # UserAccount entity → useraccount table
│   │   │   └── user_session.py     # UserSession entity → usersession table
│   │   ├── services/
│   │   │   ├── auth_login_cotroller.py   # AuthLoginCotroller
│   │   │   └── auth_logout_cotroller.py  # AuthLogoutCotroller
│   │   ├── routes/
│   │   │   └── auth_routes.py      # POST /api/auth/login, POST /api/auth/logout
│   │   └── utils/
│   │       └── auth_utils.py       # token_required decorator
│   ├── migrations/
│   │   └── 001_create_tables.sql   # useraccount + usersession tables
│   ├── tests/
│   │   └── test_auth.py            # 16 unit tests (Jiecheng)
│   ├── seed.py                     # 100+ test users
│   ├── run.py
│   └── requirements.txt
├── docs/                       # UML diagrams (Aprial)
├── meeting-minutes/            # Sprint records (Linn)
├── screenshots/                # Taiga board evidence (Linn)
└── README.md
```

## Database tables (csit314)

### useraccount
| Column        | Type                                                    |
|---------------|---------------------------------------------------------|
| user_id       | INT(8) PK AUTO_INCREMENT                               |
| username      | VARCHAR(50) UNIQUE NOT NULL                            |
| password_hash | VARCHAR(255) NOT NULL                                  |
| isActive      | TINYINT(1) NOT NULL DEFAULT 1                          |
| role          | ENUM('admin','fund_raiser','donee','platform_manager') |
| created_at    | DATETIME DEFAULT CURRENT_TIMESTAMP                     |

### usersession
| Column      | Type                              |
|-------------|-----------------------------------|
| session_id  | INT(8) PK AUTO_INCREMENT          |
| user_id     | INT(8) FK → useraccount.user_id   |
| token       | VARCHAR(64) UNIQUE NOT NULL       |
| login_time  | DATETIME DEFAULT CURRENT_TIMESTAMP|
| logout_time | DATETIME NULL                     |
| expires_at  | DATETIME NOT NULL                 |
| status      | ENUM('active','expired')          |

## Quick start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt

# Edit .env — set your MySQL password
cp .env .env.local

# Create tables
mysql -u root -p < migrations/001_create_tables.sql

# Seed 100+ test users
python seed.py

# Run
python run.py
# API runs at http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# App runs at http://localhost:5173
```

## Test accounts
| Username    | Password  | Role             | isActive |
|-------------|-----------|------------------|----------|
| admin01     | admin123  | admin            | 1        |
| fr01        | fr123     | fund_raiser      | 1        |
| donee01     | donee123  | donee            | 1        |
| pm01        | pm123     | platform_manager | 1        |
| suspended01 | test123   | donee            | 0        |

## API endpoints (Sprint 1)
| Method | URL                  | Auth     | Description              |
|--------|----------------------|----------|--------------------------|
| POST   | /api/auth/login      | None     | Login, returns token     |
| POST   | /api/auth/logout     | Bearer   | Expire session           |
| GET    | /api/auth/me         | Bearer   | Get current user info    |

## Run tests (TDD evidence for Jiecheng)
```bash
cd backend
pytest tests/test_auth.py -v
```
Screenshot the output and save to `screenshots/` as TDD evidence.

## Team ownership
| File/Folder                         | Owner    |
|-------------------------------------|----------|
| app/models/                         | Zilin    |
| app/services/                       | Sylvia   |
| app/routes/                         | Sylvia   |
| app/utils/                          | Sylvia   |
| migrations/ + seed.py               | Zilin    |
| tests/                              | Jiecheng |
| frontend/src/pages/ + components/   | Yimin    |
| frontend/src/services/              | Yimin    |
| docs/ (UML diagrams)                | Aprial   |
| meeting-minutes/ + screenshots/     | Linn     |
