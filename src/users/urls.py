from django.urls import path

from .views import UserCreate, UserProfile, PasswordChange

app_name = "user"

urlpatterns = [
    path('add/', UserCreate.as_view(), name="add"),
    path('update/<int:pk>', UserProfile.as_view(), name="update"),
    path('password/change', PasswordChange.as_view(), name="password")
]
