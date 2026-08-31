# System Understanding Document

## 1. Code Architecture & Component Locations

* **FastAPI Application Entry Point:** `app/main.py`
* **API Routers Registration:** `app/api/v1/api.py` (or `app/api/router.py`)
* **Environment Variables Loading:** `app/core/config.py` (using Pydantic `BaseSettings`)
* **Database Session Configuration:** `app/core/database.py` (SQLAlchemy `engine` & `SessionLocal`)
* **SQLAlchemy Models:** `app/models/` (e.g., `user.py`, `report.py`)
* **Pydantic Schemas:** `app/schemas/` (Data validation and serialization)
* **JWT Generation & Validation:** `app/core/security.py`
* **User Dependencies & Role Permissions:** `app/api/deps.py` (`get_current_user`, `require_role`)
* **Report Business Logic:** `app/services/report_service.py`
* **Report Status Definitions:** Defined in `app/models/report.py` (Enum) and `app/schemas/report.py`
* **Seed Data Script:** `scripts/seed.py`
* **Automated Tests Location:** `tests/`

---

## 2. Folder Structure Purpose

* **`app/api`**: Houses HTTP endpoints/routers, request handling, and dependency injection (`deps.py`).
* **`app/core`**: Contains system-wide configurations, database connections, and security/JWT utilities.
* **`app/models`**: Defines database tables and ORM entities using SQLAlchemy.
* **`app/schemas`**: Defines Pydantic data schemas for request validation and response formatting.
* **`app/services`**: Implements core business logic and database interactions separated from HTTP endpoints.

---

## 3. Database Entities & Relationships

* **User**: Stores system users (Citizens, Employees, Admins).
* **Report**: Represents submitted civic issues. Linked to `User` via `citizen_id` (creator) and `assigned_employee_id` (handler).
* **ActivityLog / Comment**: Tracks state changes and updates on reports. Linked to `Report` and `User`.

---

## 4. User Roles & Capabilities

* **Citizen**: Create reports (description >= 20 chars), track their own reports (`IRQ-2026-XXXX`), view public updates.
* **Staff / Employee**: Review assigned reports, update report status, add official comments, search/filter reports, export data (CSV).
* **Admin**: View full analytics dashboard, manage user roles, review activity logs, archive reports without hard deletion.

---

## 5. Report Lifecycle & Workflow

1. **Creation**: Citizen submits a report $\rightarrow$ System validates input $\rightarrow$ Assigns `NEW` status and generates tracking ID (`IRQ-2026-XXXX`).
2. **Review & Assignment**: Staff/Admin reviews report $\rightarrow$ Status changes to `IN_REVIEW` $\rightarrow$ Assigned to an Employee.
3. **Execution**: Employee works on issue $\rightarrow$ Status updated to `IN_PROGRESS`.
4. **Resolution & Closure**: Issue resolved $\rightarrow$ Status changed to `RESOLVED` $\rightarrow$ Citizen/Admin verifies and sets status to `CLOSED`.

---

## 6. Request Cycle Flow Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Citizen as Citizen (Client)
    participant API as Router (app/api)
    participant Auth as Security (app/api/deps.py)
    participant Service as Report Service (app/services)
    participant DB as Database (PostgreSQL)

    Citizen->>API: POST /api/v1/reports (JWT + Payload)
    API->>Auth: Validate Token & Citizen Role
    Auth-->>API: Authorized User Context
    API->>Service: create_report(db, report_in, user_id)
    Service->>DB: INSERT INTO reports
    DB-->>Service: Saved Report Entity
    Service-->>API: Processed Report Data
    API-->>Citizen: 201 Created (Report Schema Response)