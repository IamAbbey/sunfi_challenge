from django.urls import path

from .views import CustomTokenObtainPairView, UserCreateView, UserListView



urlpatterns = [
    path("auth/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("signup/", UserCreateView.as_view(), name="user_create"),
    path("list/", UserListView.as_view(), name="user_list"),
]
