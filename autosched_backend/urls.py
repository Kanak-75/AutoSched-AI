from django.contrib import admin
from django.urls import path

from scheduler_core.views import ScheduleView
from scheduler_core.views_auth import LoginView, SignUpView
from scheduler_core.views_frontend import FrontendView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/signup/", SignUpView.as_view(), name="signup"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/schedule/", ScheduleView.as_view(), name="schedule"),
    path("", FrontendView.as_view(), name="frontend"),  # Root URL serves frontend
]


