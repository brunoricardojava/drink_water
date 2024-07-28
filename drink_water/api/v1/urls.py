from django.urls import re_path

from drink_water.views import UserCreateView

urlpatterns = [
    re_path(r"user/?$", UserCreateView.as_view(), name="Create User"),
]
