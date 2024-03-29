"""smiap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from logging import DEBUG

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(("api_v1.urls", "api_v1"), namespace="api-v1")),
    path("", include("main.urls", namespace="")),
    path("", include(("news.urls", "news"), namespace="news")),
    # Plugins
    path("", include("django.contrib.flatpages.urls")),
    # Deprecated. Now it's just flatpage /students
    # path("students/", include(("schedule.urls", "schedule"), namespace="schedule")),
]

if DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        *static(settings.STATIC_URL or "/static", document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ] + urlpatterns  # type: ignore
