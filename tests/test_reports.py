"""
tests/test_reports.py
Report management tests.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.area import Area
from app.models.category import ServiceCategory
from app.models.governorate import Governorate
from app.models.user import User
from tests.conftest import auth_header, get_token


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def create_report_payload(
    category_id: int,
    governorate_id: int,
    area_id: int,
    title: str = "Test report title here",
    description: str = "Test report description with enough detail.",
) -> dict:
    return {
        "category_id": category_id,
        "governorate_id": governorate_id,
        "area_id": area_id,
        "title": title,
        "description": description,
        "address_details": "Some street, block 1",
    }


def post_report(
    client: TestClient,
    token: str,
    category: ServiceCategory,
    governorate: Governorate,
    area: Area,
) -> dict:
    resp = client.post(
        "/api/v1/reports",
        json=create_report_payload(category.id, governorate.id, area.id),
        headers=auth_header(token),
    )
    assert resp.status_code == 201, resp.json()
    return resp.json()


# ---------------------------------------------------------------------------
# Citizen creates a report
# ---------------------------------------------------------------------------

class TestCreateReport:
    def test_citizen_cannot_create_urgent_report(
        self,
        client: TestClient,
        citizen: User,
        category: ServiceCategory,
        governorate: Governorate,
        area: Area,
    ):
        """تأكيد منع المواطن من إنشاء بلاغ بأولوية عاجلة."""
        token = get_token(client, citizen.email)
        payload = create_report_payload(category.id, governorate.id, area.id)
        payload["priority"] = "urgent"

        response = client.post(
            "/api/v1/reports",
            headers=auth_header(token),
            json=payload,
        )
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# Citizen views reports
# ---------------------------------------------------------------------------

class TestViewReport:
    def test_citizen_views_report(
        self,
        client: TestClient,
        citizen: User,
        category: ServiceCategory,
        governorate: Governorate,
        area: Area,
    ):
        token = get_token(client, citizen.email)
        created = post_report(client, token, category, governorate, area)
        report_id = created["id"]

        resp = client.get(f"/api/v1/reports/{report_id}", headers=auth_header(token))
        assert resp.status_code == 200
        assert resp.json()["id"] == report_id


# ---------------------------------------------------------------------------
# Urgent Reports Change Request Tests
# ---------------------------------------------------------------------------

class TestUrgentReportsFilters:
    def test_admin_list_urgent_only_filter(self, client: TestClient, admin: User):
        token = get_token(client, admin.email)
        resp = client.get("/api/v1/admin/reports?urgent_only=true", headers=auth_header(token))
        assert resp.status_code == 200

    def test_employee_list_urgent_only_filter(self, client: TestClient, employee: User):
        token = get_token(client, employee.email)
        resp = client.get("/api/v1/employee/reports?urgent_only=true", headers=auth_header(token))
        assert resp.status_code == 200

    def test_dashboard_stats_includes_urgent_count(self, client: TestClient, admin: User):
        token = get_token(client, admin.email)
        resp = client.get("/api/v1/admin/dashboard/stats", headers=auth_header(token))
        assert resp.status_code == 200
        assert "urgent_reports" in resp.json()