from logging import DEBUG

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("admin/", admin.site.urls),
    path("api/v1/", include(("api_v1.urls", "api_v1"), namespace="api-v1")),
    path("materials/", include(("news.urls", "news"), namespace="news")),
    path("students/", include(("schedule.urls", "schedule"), namespace="schedule")),
    path("", include("main.urls", namespace="")),
    path("", include("django.contrib.flatpages.urls")),
]

if DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        *static(settings.STATIC_URL or "/static", document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ] + urlpatterns  # type: ignore
