import pytest
from django.urls import reverse
from rest_framework import status

from tests.conftest import *


@pytest.mark.django_db
@pytest.mark.xfail
def test_unauthorized_request(unauthenticated_client):
    url = reverse("token_obtain_pair")
    response = unauthenticated_client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_all_user(authenticated_client):
    url = reverse("user_list")
    response = authenticated_client().get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"]
    assert len(response.data["data"]) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email, password, username, status_code",
    [
        pytest.param(None, None, None, 400, marks=pytest.mark.bad_request),
        pytest.param(
            None,
            "strong_pass",
            None,
            400,
            marks=pytest.mark.bad_request,
        ),
        pytest.param(
            "some@magic.email",
            None,
            None,
            400,
            marks=[pytest.mark.bad_request],
        ),
        pytest.param(
            "user@example.com",
            "strong_pass",
            None,
            400,
            marks=[pytest.mark.bad_request],
        ),
        pytest.param(
            "user@example.com",
            "strong_pass",
            "username",
            201,
            marks=pytest.mark.success_request,
        ),
    ],
)
def test_create_user(email, password, username, status_code, unauthenticated_client):
    url = reverse("user_create")
    data = {
        "password": password,
        "username": username,
        "email": email,
    }
    response = unauthenticated_client.post(url, data, format="json")
    print(response.data)
    assert response.status_code == status_code
