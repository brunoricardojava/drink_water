from django.urls import re_path

from drink_water.views import UserCreateView, UserActionView

urlpatterns = [
    re_path(r"user/?$", UserCreateView.as_view(), name="Create User"),
    re_path(r"user/(?P<user_id>[0-9]+)/action/?$", UserActionView.as_view(), name= "Actions of user")
]
