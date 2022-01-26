from rest_framework import serializers

from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):

    link = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_date",
            "favorite_by",
        )

    def create(self, validated_data):
        favorite = Favorite.objects.create(**validated_data)
        return favorite

    def update(self, instance, validated_data): # pragma: no cover

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def get_link(self, obj):
        if obj.is_quote:
            return f"/api/quote/{obj.quote_id}"
        else:
            return f"/api/character/{obj.character_id}"
