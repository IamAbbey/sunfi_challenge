from uuid import uuid4

from django.db import models


class Favorite(models.Model):

    character_id = models.CharField(
        max_length=200,
    )
    quote_id = models.CharField(max_length=200, blank=True, null=True)
    favorite_by = models.ForeignKey(
        to="authentication.CustomUser",
        on_delete=models.CASCADE,
    )
    is_quote = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        f"{self.character_id}"
