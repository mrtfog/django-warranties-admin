from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("apps.users.urls")),
    path("api/billing/", include("apps.billing.urls")),
    path("api/automation/", include("apps.automation.urls")),
]
