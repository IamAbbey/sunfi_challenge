import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Favorite
from .serializers import FavoriteSerializer



url = settings.THE_ONE_API_BASE_URL

def get_requests(url): # pragma: no cover
    if settings.THE_ONE_API_KEY is None:
        return "settings.THE_ONE_API_KEY needs to be set"
    headers = {"Authorization": "Bearer " + settings.THE_ONE_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        json_response = response.text
    else:
        json_response = response.json()
    return json_response


class AddFavoriteCharacter(APIView):
    """
    A viewset for viewing and editing favorite instances.
    """

    # I am of the opinion that the character id to be added as
    # favorite ought to be passed in as a request body
    # Contrary to the instruction given, which passes the character id from the url
    def post(self, request, character_id):
        serializer = FavoriteSerializer(
            data={"character_id": character_id},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(favorite_by=self.request.user)

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED
        )


class AddFavoriteCharacterQuote(APIView):
    """
    A viewset for viewing and editing favorite instances.
    """

    # I am of the opinion that the character_id and quote_id to be added as
    # favorite ought to be passed in as a request body
    # Contrary to the instruction given, which passes the character id from the url
    def post(self, request, character_id, quote_id):
        serializer = FavoriteSerializer(
            data={"character_id": character_id, "quote_id": quote_id, "is_quote": True},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(favorite_by=self.request.user)

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED
        )


class FavoriteListView(APIView):
    """
    Perform GET operation to list all characters gotten from THE ONE API
    """

    def get(self, request):
        favorites = Favorite.objects.filter(favorite_by=self.request.user)
        serializer = FavoriteSerializer(favorites, many=True)

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


class CharacterListView(APIView):
    """
    Perform GET operation to list all characters gotten from THE ONE API
    """

    def get(self, request):
        response = get_requests(f"{url}/character")

        return Response({"success": True, "data": response}, status=status.HTTP_200_OK)


class CharacterDetailView(APIView):
    """
    Perform GET operation to get a character's information gotten from THE ONE API
    """

    def get(self, request, character_id):
        response = get_requests(f"{url}/character/{character_id}")

        return Response({"success": True, "data": response}, status=status.HTTP_200_OK)


class CharacterQuotesListView(APIView):
    """
    Perform GET operation to list a character's quote gotten from THE ONE API
    """

    def get(self, request, character_id):
        response = get_requests(f"{url}/character/{character_id}/quote")

        return Response({"success": True, "data": response}, status=status.HTTP_200_OK)


class CharacterQuotesDetailView(APIView):
    """
    Perform GET operation to get a character's quote information gotten from THE ONE API
    """

    def get(self, request, quote_id):
        response = get_requests(f"{url}/quote/{quote_id}")

        return Response({"success": True, "data": response}, status=status.HTTP_200_OK)
