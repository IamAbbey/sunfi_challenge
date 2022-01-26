from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .serializers import CustomTokenObtainPairSerializer, CustomUserSerializer


class UserCreateView(generics.CreateAPIView):
    """
    Create user endpoint
    """

    serializer_class = CustomUserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        response = super().create(request)
        return Response(
            {"success": True, "data": response.data}, status=status.HTTP_201_CREATED
        )



class UserListView(generics.ListAPIView):
    """
    Returns all active users
    """

    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = CustomUserSerializer

    def list(self, request, *args, **kwargs):
        """
        GET verb, to return all active users
        """
        queryset = self.get_queryset()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Authentication endpoint to get access tokens
    """

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = CustomTokenObtainPairSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        response_payload = serializer.validated_data
        return Response(
            {"success": True, "data": response_payload}, status=status.HTTP_200_OK
        )
