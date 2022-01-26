from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }
        exclude = (
            "groups",
            "user_permissions",
        )
        read_only_fields = (
            "id",
            "is_superuser",
            "is_active",
            "is_staff",
            "last_login",
            "date_joined",
        )

    def create(self, validated_data):
        customuser = CustomUser.objects.create_user(**validated_data)
        return customuser

    def update(self, instance, validated_data): # pragma: no cover
        password = validated_data.pop("password", None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = CustomUser.EMAIL_FIELD


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data
