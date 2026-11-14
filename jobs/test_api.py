import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_job():
    client = APIClient()
    response = client.post(
        "/api/jobs/",
        {"company": "NVIDIA", "title": "Software Engineering Student"},
        format="json",
    )
    assert response.status_code == 201
    assert response.data["company"] == "NVIDIA"


@pytest.mark.django_db
def test_duplicate_job_is_rejected():
    client = APIClient()
    response1 = client.post(
        "/api/jobs/",
        {"company": "NVIDIA", "title": "Software Engineering Student"},
        format="json",
    )
    response2 = client.post(
        "/api/jobs/",
        {"company": "NVIDIA", "title": "Software Engineering Student"},
        format="json",
        )
    assert response1.status_code == 201
    assert response2.status_code == 400


@pytest.mark.django_db
def test_analyze_returns_fit_score():
    client = APIClient()
    response = client.post(
        "/api/analyze/",
        {"text": "Student in Haifa. Python and Verilog."},
        format="json",
        )
    assert response.status_code == 200
    assert response.data["fit_score"] == 50


@pytest.mark.django_db
def test_analyze_without_text():
    client = APIClient()
    response = client.post(
        "/api/analyze/",
        {},
        format="json",
        )
    assert response.status_code == 400