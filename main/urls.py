from django.contrib.flatpages import views
from django.urls import path, register_converter
from django.views.generic import RedirectView

from main.views.history_view import HistoryView
from main.views.index_view import IndexView
from main.views.link_view import LinkView
from main.views.profile_view import ProfileDescriptionView, ProfilePublicationsView
from main.views.publications_view import PublicationView
from main.views.staff_view import StaffView
from news import converters

register_converter(converters.FourDigitYearConverter, "yyyy")
register_converter(converters.TwoDigitConverter, "mm")
register_converter(converters.TwoDigitConverter, "dd")
register_converter(converters.ActivateCodeConverter, "key")

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path(
        "important-message",
        views.flatpage,
        {"url": "/important-message"},
        name="important-message",
    ),
    path(
        "abiturients/info",
        views.flatpage,
        {"url": "/abiturients/info"},
        name="abiturients",
    ),
    path(
        "abiturients/programs",
        views.flatpage,
        {"url": "/abiturients/programs"},
        name="programs",
    ),
    path("about", RedirectView.as_view(pattern_name="intro")),
    path("about/intro", views.flatpage, {"url": "/about/intro"}, name="intro"),
    path(
        "about/conferences",
        views.flatpage,
        {"url": "/about/conferences"},
        name="conferences",
    ),
    path("about/history", HistoryView.as_view(), name="history"),
    path("about/history/page<int:number>", HistoryView.as_view(), name="history"),
    path("about/staff", StaffView.as_view(), name="staff"),
    path("about/contacts", views.flatpage, {"url": "/about/contacts"}, name="contacts"),
    path(
        "materials/tutorials",
        views.flatpage,
        {"url": "/materials/tutorials"},
        name="tutorials",
    ),
    path("materials/publications", PublicationView.as_view(), name="publications"),
    path("f/<str:link>", LinkView.as_view(), name="short-file"),
    path(
        "profile/<int:profile>/description",
        ProfileDescriptionView.as_view(),
        name="profile-description",
    ),
    path(
        "profile/<int:profile>/publications",
        ProfilePublicationsView.as_view(),
        name="profile-publications",
    ),
    # Redirects from old url.
    path("programs", RedirectView.as_view(pattern_name="programs")),
    path("conferences", RedirectView.as_view(pattern_name="conferences")),
    path("abiturients", RedirectView.as_view(pattern_name="abiturients")),
    path("materials", RedirectView.as_view(pattern_name="news:news-list")),
    path("materials/news", RedirectView.as_view(pattern_name="news:news-list")),
    path("materials/timetable", RedirectView.as_view(pattern_name="timetable")),
    path(
        "materials/timetable/extramural",
        RedirectView.as_view(pattern_name="timetable-extramural"),
    ),
    path("students", views.flatpage, {"url": "/students"}, name="students"),
    # Temp redirects from deprecated schedule
    path(
        "students/timetable",
        RedirectView.as_view(pattern_name="students"),
        name="timetable",
    ),
    path(
        "students/timetable/extramural",
        RedirectView.as_view(pattern_name="students"),
        name="timetable-extramural",
    ),
    path(
        "students/session",
        RedirectView.as_view(pattern_name="students"),
        name="timetable-session",
    ),
    path(
        "students/timetable/ex-session",
        RedirectView.as_view(pattern_name="students"),
        name="timetable-extramural-session",
    ),
]
