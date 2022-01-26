import pytest
from django.urls import reverse
from rest_framework import status

from tests.conftest import *


@pytest.mark.django_db
def test_get_all_favorite(authenticated_client, create_user, create_favorite_character):
    url = reverse("favorite_list")
    unhashed_password, user = create_user(password="test-pass")
    create_favorite_character(user)
    response = authenticated_client(
        create_new_user=False, user=user, unhashed_password=unhashed_password
    ).get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"]
    assert len(response.data["data"]) == 1


@pytest.mark.django_db
def test_add_character_favorite(
    authenticated_client, create_user, create_favorite_character
):
    url = reverse(
        "add_character_favorite", kwargs={"character_id": "5cd99d4bde30eff6ebccfd0d"}
    )
    client = authenticated_client()
    response = client.post(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["success"]
    assert response.data["data"]["character_id"] == "5cd99d4bde30eff6ebccfd0d"

    url = reverse("favorite_list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"]
    assert len(response.data["data"]) == 1


@pytest.mark.django_db
def test_add_quote_favorite(
    authenticated_client, create_user, create_favorite_character
):
    url = reverse(
        "add_quote_favorite",
        kwargs={
            "character_id": "5cd99d4bde30eff6ebccfd0d",
            "quote_id": "5cd96e05de30eff6ebcce7fe",
        },
    )
    client = authenticated_client()
    response = client.post(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["success"]
    assert response.data["data"]["character_id"] == "5cd99d4bde30eff6ebccfd0d"
    assert response.data["data"]["quote_id"] == "5cd96e05de30eff6ebcce7fe"
    assert response.data["data"]["is_quote"]

    url = reverse("favorite_list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"]
    assert len(response.data["data"]) == 1


@pytest.mark.django_db
def test_get_quote_detail(authenticated_client, mocker):
    url = reverse("quote_detail", kwargs={"quote_id": "5cd96e05de30eff6ebcce7fe"})
    mock_requests = mocker.patch("apps.favorite.views.get_requests")
    mock_requests.return_value = {
        "docs": [
            {
                "_id": "5cd96e05de30eff6ebcce7fe",
                "dialog": "Haven't you had any sleep Mr Frodo?",
                "movie": "5cd95395de30eff6ebccde5d",
                "character": "5cd99d4bde30eff6ebccfd0d",
            }
        ],
        "total": 1,
        "limit": 1000,
        "offset": 0,
        "page": 1,
        "pages": 1,
    }
    response = authenticated_client().get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"]


@pytest.mark.django_db
def test_get_character_detail(authenticated_client, mocker):
    url = reverse(
        "character_detail", kwargs={"character_id": "5cd99d4bde30eff6ebccfd0d"}
    )
    mock_requests = mocker.patch("apps.favorite.views.get_requests")
    mock_requests.return_value = {
        "docs": [
            {
                "_id": "5cd99d4bde30eff6ebccfd0d",
                "height": "1.22m (4'0\")",
                "race": "Hobbit",
                "gender": "Male",
                "birth": "April 6 ,2980",
                "spouse": "Rosie Cotton",
                "death": "Still alive, after going to the ,Undying Lands, in ,FO 61",
                "realm": "",
                "hair": "Blond (movie)",
                "name": "Samwise Gamgee",
                "wikiUrl": "http://lotr.wikia.com//wiki/Samwise_Gamgee",
            }
        ],
        "total": 1,
        "limit": 1000,
        "offset": 0,
        "page": 1,
        "pages": 1,
    }
    response = authenticated_client().get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"]


@pytest.mark.django_db
def test_get_character_quote_list(authenticated_client, mocker):
    url = reverse(
        "character_quote_list", kwargs={"character_id": "5cd99d4bde30eff6ebccfd0d"}
    )
    mock_requests = mocker.patch("apps.favorite.views.get_requests")
    mock_requests.return_value = {
        "docs": [
            {
                "_id": "5cd96e05de30eff6ebcce7fe",
                "dialog": "Haven't you had any sleep Mr Frodo?",
                "movie": "5cd95395de30eff6ebccde5d",
                "character": "5cd99d4bde30eff6ebccfd0d",
            },
            {
                "_id": "5cd96e05de30eff6ebcce801",
                "dialog": "Not before Mr Frodo's had something to eat.",
                "movie": "5cd95395de30eff6ebccde5d",
                "character": "5cd99d4bde30eff6ebccfd0d",
            },
        ]
    }
    response = authenticated_client().get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"]
    assert len(response.data["data"]["docs"]) == 2


@pytest.mark.django_db
def test_get_character_list(authenticated_client, mocker):
    url = reverse("character_list")
    mock_requests = mocker.patch("apps.favorite.views.get_requests")
    mock_requests.return_value = {
        "docs": [
            {
                "_id": "5cd99d4bde30eff6ebccfbbe",
                "height": "",
                "race": "Human",
                "gender": "Female",
                "birth": "",
                "spouse": "Belemir",
                "death": "",
                "realm": "",
                "hair": "",
                "name": "Adanel",
                "wikiUrl": "http://lotr.wikia.com//wiki/Adanel",
            },
            {
                "_id": "5cd99d4bde30eff6ebccfbbf",
                "height": "",
                "race": "Human",
                "gender": "Male",
                "birth": "Before ,TA 1944",
                "spouse": "",
                "death": "Late ,Third Age",
                "realm": "",
                "hair": "",
                "name": "Adrahil I",
                "wikiUrl": "http://lotr.wikia.com//wiki/Adrahil_I",
            },
        ]
    }
    response = authenticated_client().get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"]
    assert len(response.data["data"]["docs"]) == 2


# @pytest.mark.django_db
# @pytest.mark.parametrize(
#     "email, password, username, status_code",
#     [
#         pytest.param(None, None, None, 400, marks=pytest.mark.bad_request),
#         pytest.param(
#             None,
#             "strong_pass",
#             None,
#             400,
#             marks=pytest.mark.bad_request,
#         ),
#         pytest.param(
#             "some@magic.email",
#             None,
#             None,
#             400,
#             marks=[pytest.mark.bad_request],
#         ),
#         pytest.param(
#             "user@example.com",
#             "strong_pass",
#             None,
#             400,
#             marks=[pytest.mark.bad_request],
#         ),
#         pytest.param(
#             "user@example.com",
#             "strong_pass",
#             "username",
#             201,
#             marks=pytest.mark.success_request,
#         ),
#     ],
# )
# def test_create_user(
#     email, password, username, status_code, unauthenticated_client
# ):
#     url = reverse("user_create")
#     data = {
#         "password": password,
#         "username": username,
#         "email": email,
#     }
#     response = unauthenticated_client.post(url, data, format="json")
#     print(response.data)
#     assert response.status_code == status_code
