import pytest
from apps.authentication.models import CustomUser
from apps.favorite.models import Favorite
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture(scope="function")
def unauthenticated_client():
    return APIClient()


@pytest.fixture(scope="function")
def test_password():
    return "strong-test-password"


@pytest.fixture(scope="function")
def test_email():
    return "test@test.com"


@pytest.fixture(scope="function")
def test_username():
    return "test-username"


@pytest.fixture(scope="function")
def create_user(
    db,
    test_password,
    test_email,
    test_username,
):
    def make_user(emailPasswordNotSupplied=True, **kwargs):

        if emailPasswordNotSupplied:
            if "password" not in kwargs:
                kwargs["password"] = test_password
            if "email" not in kwargs:
                kwargs["email"] = test_email
            if "username" not in kwargs:
                kwargs["email"] = test_username

        user = CustomUser.objects.create_user(
            **kwargs,
        )
        user.set_password(kwargs["password"])
        user.save()
        return kwargs["password"], user

    return make_user


@pytest.fixture(scope="function")
def get_token():
    def a_token(user_obj, unhashed_password):
        url = reverse("token_obtain_pair")
        data = {
            "email": user_obj.email,
            "password": unhashed_password,
        }
        client = APIClient()
        res = client.post(url, data=data, format="json")
        access_token = res.json()["data"]["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        return client

    return a_token


@pytest.fixture(scope="function")
def authenticated_client(db, create_user, get_token):
    def prepare_client(
        unauthorized_token=False,
        create_new_user=True,
        user=None,
        unhashed_password=None,
    ):
        if unauthorized_token:  # pragma: no cover
            return APIClient()
        if create_new_user or user is None or unhashed_password is None:
            unhashed_password, user = create_user()

        return get_token(user, unhashed_password)

    return prepare_client


@pytest.fixture(scope="function")
def login_as_user(db, get_token):  # pragma: no cover
    def prepare_client(user, unhashed_password, unauthorized_token=False):
        if unauthorized_token:
            return APIClient()

        return get_token(user, unhashed_password)

    return prepare_client


@pytest.fixture(scope="function")
def create_favorite_character(db):
    def prepare_response(user):

        return Favorite.objects.create(
            favorite_by=user, character_id="test-character-id"
        )

    return prepare_response
