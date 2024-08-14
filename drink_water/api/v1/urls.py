from django.urls import re_path

from drink_water.views import UserView, UserActionView, UserGoalsView

urlpatterns = [
    re_path(r"user/?(?P<user_id>[0-9]+)?/?$", UserView.as_view(), name="UserRoute"),
    re_path(r"user/(?P<user_id>[0-9]+)/action/?$", UserActionView.as_view(), name="UserActionRoute"),
    re_path(r"user/(?P<user_id>[0-9]+)/goal/?$", UserGoalsView.as_view(), name="UserGoalRoute"),
]
