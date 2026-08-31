# Khidmati Iraq – Backend API

A platform where Iraqi citizens can report public-service problems such as electricity outages, water problems, damaged roads, waste accumulation, broken streetlights, and sewage issues.

Built as a teaching project for software engineering students at the university level.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Prerequisites](#prerequisites)
4. [PostgreSQL Database Creation](#postgresql-database-creation)
5. [PowerShell Setup](#powershell-setup)
6. [Environment Configuration](#environment-configuration)
7. [Migration Commands](#migration-commands)
8. [Seed Command](#seed-command)
9. [Application Start](#application-start)
10. [Tests](#tests)
11. [Swagger Documentation](#swagger-documentation)
12. [Development Credentials](#development-credentials)
13. [Project Structure](#project-structure)
14. [Roles and Permissions](#roles-and-permissions)
15. [Report Workflow](#report-workflow)
16. [API Endpoints](#api-endpoints)
17. [Common Troubleshooting](#common-troubleshooting)

---

## Project Overview

Khidmati Iraq is a simple REST API that allows:

- **Citizens** to submit, track, update, and cancel public-service problem reports.
- **Employees** (municipal workers) to review and process reports within their governorate.
- **Admins** to manage users, assign reports, change priorities, and view dashboard statistics.

---

## Technology Stack

| Technology        | Version  | Purpose                        |
|-------------------|----------|--------------------------------|
| Python            | 3.12     | Programming language           |
| FastAPI           | 0.115    | Web framework                  |
| PostgreSQL        | 14+      | Relational database            |
| SQLAlchemy        | 2.0      | ORM                            |
| Alembic           | 1.14     | Database migrations            |
| Pydantic          | v2       | Data validation                |
| python-jose       | 3.3      | JWT tokens                     |
| pwdlib / Argon2   | 0.2      | Password hashing               |
| Pytest            | 8.3      | Testing                        |
| httpx             | 0.28     | Async HTTP client for tests    |

---

## Prerequisites

- Python 3.12 installed (`py -3.12 --version`)
- PostgreSQL installed and running locally
- `psql` available in the terminal

---

## PostgreSQL Database Creation

Open **psql** or your preferred PostgreSQL client and run:

```sql
-- Development database
CREATE DATABASE khidmati_iraq;

-- Test database (required for running tests)
CREATE DATABASE khidmati_iraq_test;
```

Or use the command line:

```powershell
psql -U postgres -c "CREATE DATABASE khidmati_iraq;"
psql -U postgres -c "CREATE DATABASE khidmati_iraq_test;"
```

---

## PowerShell Setup

Run the automated setup script from the project root:

```powershell
.\setup.ps1
```

Or run the steps manually:

```powershell
# 1. Create and activate the virtual environment
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3. Copy the environment file
Copy-Item .env.example .env
```

---

## Environment Configuration

Edit `.env` after the setup:

```env
APP_NAME=Khidmati Iraq API
APP_ENV=development
DEBUG=true
API_V1_PREFIX=/api/v1

DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/khidmati_iraq

JWT_SECRET_KEY=change-this-secret-key-before-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

SEED_DEFAULT_PASSWORD=ChangeMe123!

TEST_DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/khidmati_iraq_test
```

> **Important**: Change `JWT_SECRET_KEY` to a long random string before any real deployment.

---

## Migration Commands

```powershell
# Apply all migrations (run this after setup)
alembic upgrade head

# Create a new migration after changing a model
alembic revision --autogenerate -m "describe your change here"

# Roll back one migration
alembic downgrade -1

# View migration history
alembic history
```

---

## Seed Command

Populate the database with governorates, areas, categories, test accounts, and sample reports:

```powershell
python -m scripts.seed
```

The seed script is **safe to run multiple times** – it uses get-or-create logic.

---

## Application Start

```powershell
uvicorn app.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

---

## Tests

Make sure `TEST_DATABASE_URL` is set in `.env` and the test database exists, then:

```powershell
pytest

# With verbose output
pytest -v

# Run only authentication tests
pytest tests/test_auth.py -v

# Run only report tests
pytest tests/test_reports.py -v
```

---

## Swagger Documentation

Interactive API documentation is available at:

```
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```
http://127.0.0.1:8000/redoc
```

---

## Development Credentials

After running the seed script, you can log in with these accounts:

| Role     | Email                            | Password       |
|----------|----------------------------------|----------------|
| Admin    | admin@khidmati.local             | ChangeMe123!   |
| Employee | employee.baghdad@khidmati.local  | ChangeMe123!   |
| Employee | employee.basra@khidmati.local    | ChangeMe123!   |
| Citizen  | citizen1@khidmati.local          | ChangeMe123!   |
| Citizen  | citizen2@khidmati.local          | ChangeMe123!   |

---

## Project Structure

```
khidmati-iraq-backend/
│
├── app/
│   ├── main.py                # FastAPI app entry point
│   ├── config.py              # Settings loaded from .env
│   ├── database.py            # SQLAlchemy engine and session
│   │
│   ├── core/
│   │   ├── security.py        # Password hashing and JWT utilities
│   │   ├── dependencies.py    # FastAPI auth dependencies (role guards)
│   │   └── exceptions.py      # Custom HTTP exceptions
│   │
│   ├── models/                # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── governorate.py
│   │   ├── area.py
│   │   ├── category.py
│   │   ├── report.py
│   │   ├── comment.py
│   │   └── status_history.py
│   │
│   ├── schemas/               # Pydantic v2 request/response schemas
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── location.py
│   │   ├── category.py
│   │   ├── report.py
│   │   └── comment.py
│   │
│   ├── services/              # Business logic
│   │   ├── auth_service.py
│   │   └── report_service.py
│   │
│   └── api/
│       ├── router.py          # Central router
│       └── v1/
│           ├── auth.py        # POST /auth/register, /login, GET /auth/me
│           ├── reference_data.py  # GET /governorates, /areas, /categories
│           ├── reports.py     # Citizen report endpoints
│           ├── employee.py    # Employee endpoints
│           └── admin.py       # Admin endpoints
│
├── alembic/                   # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── scripts/
│   ├── seed.py                # Database seed script
│   └── create_admin.py        # Interactive admin creation
│
├── tests/
│   ├── conftest.py            # Shared test fixtures
│   ├── test_auth.py           # Authentication tests
│   └── test_reports.py        # Report management tests
│
├── .env.example               # Environment variable template
├── .gitignore
├── alembic.ini
├── requirements.txt
├── setup.ps1                  # Automated setup script
└── README.md
```

---

## Roles and Permissions

| Action                              | Citizen | Employee | Admin |
|-------------------------------------|---------|----------|-------|
| Register account                    | ✓       | –        | –     |
| Submit a report                     | ✓       | –        | –     |
| View own reports                    | ✓       | –        | –     |
| Update own report (submitted only)  | ✓       | –        | –     |
| Cancel own report                   | ✓       | –        | –     |
| View public comments                | ✓       | ✓        | ✓     |
| Add public comment                  | ✓       | ✓        | ✓     |
| View internal notes                 | –       | ✓        | ✓     |
| Add internal note                   | –       | ✓        | ✓     |
| View governorate reports            | –       | ✓        | ✓     |
| Update report status                | –       | ✓        | ✓     |
| Resolve a report                    | –       | ✓        | ✓     |
| Create employee accounts            | –       | –        | ✓     |
| Assign employee to report           | –       | –        | ✓     |
| Change report priority              | –       | –        | ✓     |
| Activate/deactivate users           | –       | –        | ✓     |
| View dashboard statistics           | –       | –        | ✓     |

---

## Report Workflow

```
[Citizen submits] ──► submitted
                         │
                    employee reviews
                         │
                    under_review ──► rejected
                         │
                    admin assigns
                         │
                      assigned
                         │
                   employee starts
                         │
                     in_progress
                         │
                   employee resolves
                         │
                      resolved
```

Citizens can cancel a report that is in `submitted` or `under_review` status.

### Status Transition Rules (employees)

| From          | To               | Actor    |
|---------------|------------------|----------|
| submitted     | under_review     | Employee |
| submitted     | rejected         | Employee |
| under_review  | assigned         | Employee |
| under_review  | rejected         | Employee |
| assigned      | in_progress      | Employee |
| in_progress   | resolved         | Employee |
| submitted     | cancelled        | Citizen  |
| under_review  | cancelled        | Citizen  |

---

## API Endpoints

### Authentication
| Method | Path                  | Description              | Auth     |
|--------|-----------------------|--------------------------|----------|
| POST   | /api/v1/auth/register | Register as citizen      | Public   |
| POST   | /api/v1/auth/login    | Login and get JWT token  | Public   |
| GET    | /api/v1/auth/me       | Get current user profile | Any user |

### Reference Data (public)
| Method | Path                                    | Description          |
|--------|-----------------------------------------|----------------------|
| GET    | /api/v1/governorates                    | List governorates    |
| GET    | /api/v1/governorates/{id}/areas         | List areas           |
| GET    | /api/v1/categories                      | List categories      |

### Citizen Reports
| Method | Path                               | Description                 |
|--------|------------------------------------|-----------------------------|
| POST   | /api/v1/reports                    | Submit a report             |
| GET    | /api/v1/reports/my                 | List my reports             |
| GET    | /api/v1/reports/{id}               | Get my report               |
| PATCH  | /api/v1/reports/{id}               | Update my report            |
| POST   | /api/v1/reports/{id}/cancel        | Cancel my report            |
| GET    | /api/v1/reports/{id}/history       | View status history         |
| GET    | /api/v1/reports/{id}/comments      | View public comments        |
| POST   | /api/v1/reports/{id}/comments      | Add a comment               |

### Employee
| Method | Path                                          | Description              |
|--------|-----------------------------------------------|--------------------------|
| GET    | /api/v1/employee/reports                      | Governorate reports      |
| GET    | /api/v1/employee/reports/assigned             | My assigned reports      |
| PATCH  | /api/v1/employee/reports/{id}/status          | Update status            |
| POST   | /api/v1/employee/reports/{id}/comments        | Add public comment       |
| POST   | /api/v1/employee/reports/{id}/internal-notes  | Add internal note        |
| POST   | /api/v1/employee/reports/{id}/resolve         | Resolve report           |

### Admin
| Method | Path                                 | Description              |
|--------|--------------------------------------|--------------------------|
| POST   | /api/v1/admin/employees              | Create employee          |
| GET    | /api/v1/admin/users                  | List all users           |
| PATCH  | /api/v1/admin/users/{id}/status      | Toggle user status       |
| GET    | /api/v1/admin/reports                | List reports (filtered)  |
| PATCH  | /api/v1/admin/reports/{id}/assign    | Assign employee          |
| PATCH  | /api/v1/admin/reports/{id}/priority  | Change priority          |
| GET    | /api/v1/admin/dashboard              | Dashboard statistics     |

---

## Common Troubleshooting

### `ModuleNotFoundError: No module named 'app'`
Make sure your virtual environment is activated and you are running commands from the project root directory:
```powershell
.\.venv\Scripts\Activate.ps1
```

### `Connection refused` or database errors
1. Make sure PostgreSQL is running.
2. Check `DATABASE_URL` in `.env` – username, password, host, port, and database name.
3. Verify the database exists:
   ```powershell
   psql -U postgres -c "\l"
   ```

### `alembic: command not found`
Activate the virtual environment first:
```powershell
.\.venv\Scripts\Activate.ps1
alembic upgrade head
```

### Migrations out of sync
If you change a model and migrations are not detected:
```powershell
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

### Tests fail with `RuntimeError: TEST_DATABASE_URL is not set`
Add `TEST_DATABASE_URL` to your `.env` file and create the test database:
```sql
CREATE DATABASE khidmati_iraq_test;
```

### Password or token errors
- JWT tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 60 minutes).
- If you change `JWT_SECRET_KEY`, all existing tokens become invalid.

---

## Create Admin Account

To create a new admin account interactively:

```powershell
python -m scripts.create_admin
```

---

## License

This project is intended for educational use. Students are encouraged to explore, modify, and extend the codebase.

## Final Submission Checklist

### Environment
* [x] My virtual environment works.
* [x] My PostgreSQL database connects.
* [x] My `.env` is not committed.
* [x] Alembic migrations run.
* [x] The seed script runs safely.
* [x] The FastAPI server starts.
* [x] Swagger opens.

### Authentication and Permissions
* [x] Registration works.
* [x] Login works.
* [x] Inactive users cannot log in.
* [x] Citizen permissions work.
* [x] Employee permissions work.
* [x] Admin permissions work.
* [x] Citizens can access only their reports.
* [x] Employees cannot access another governorate’s reports.
* [x] Internal notes are protected.

### Reports
* [x] Report creation works.
* [x] Governorate and area validation works.
* [x] Report filtering works.
* [x] Search works.
* [x] Pagination works.
* [x] Assignment validation works.
* [x] Valid status transitions work.
* [x] Invalid transitions fail.
* [x] Every status change creates history.
* [x] Resolution requires a summary.
* [x] `resolved_at` is stored.
* [x] Dashboard counts are correct.
* [x] Urgent-report requirements work.

### Quality
* [x] Automated tests pass.
* [x] Tests use a separate test database.
* [x] Swagger matches my implementation.
* [x] Documentation is complete.
* [x] Known limitations are documented.
* [x] My Git commits are clear.
* [x] My repository is pushed.
* [x] My presentation is ready.
* [x] I can explain my submitted code.
*