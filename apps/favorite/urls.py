from django.urls import path

from .views import (
    AddFavoriteCharacter,
    AddFavoriteCharacterQuote,
    CharacterDetailView,
    CharacterListView,
    CharacterQuotesDetailView,
    CharacterQuotesListView,
    FavoriteListView,
)

urlpatterns = [
    path("character/", CharacterListView.as_view(), name="character_list"),
    path("character/<str:character_id>", CharacterDetailView.as_view(), name="character_detail"),
    path("character/<str:character_id>/quote/", CharacterQuotesListView.as_view(), name="character_quote_list"),
    path("quote/<quote_id>", CharacterQuotesDetailView.as_view(), name="quote_detail"),
    path("characters/<str:character_id>/favorite/", AddFavoriteCharacter.as_view(), name="add_character_favorite"),
    path(
        "characters/<str:character_id>/quotes/<str:quote_id>/favorites/",
        AddFavoriteCharacterQuote.as_view(), name="add_quote_favorite"
    ),
    path("favorite/", FavoriteListView.as_view(), name="favorite_list"),
]
