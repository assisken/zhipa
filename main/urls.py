from django.urls import path

from main.views import News


urlpatterns = [
    path('', News.as_view(), name='news'),
]
