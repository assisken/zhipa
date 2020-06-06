from django.urls import path, register_converter
from django.views.generic import TemplateView, RedirectView

from news import converters
from .views import *

register_converter(converters.FourDigitYearConverter, 'yyyy')
register_converter(converters.TwoDigitConverter, 'mm')
register_converter(converters.TwoDigitConverter, 'dd')
register_converter(converters.ActivateCodeConverter, 'key')

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('abiturients/info', TemplateView.as_view(template_name='abiturients/info.html'), name='abiturients'),
    path('abiturients/programs', TemplateView.as_view(template_name='abiturients/programs.html'), name='programs'),

    path('about', TemplateView.as_view(template_name='about/intro.html'), name='about'),
    path('about/conferences', TemplateView.as_view(template_name='about/conferences.html'), name='programs'),
    path('about/intro', TemplateView.as_view(template_name='about/intro.html'), name='intro'),
    path('about/history', HistoryView.as_view(), name='history'),
    path('about/history/page<int:number>', HistoryView.as_view(), name='history'),
    path('about/staff', StaffView.as_view(), name='staff'),
    path('about/contacts', TemplateView.as_view(template_name='about/contacts.html'), name='contacts'),

    path('materials/tutorials', TemplateView.as_view(template_name='materials/tutorials.html'), name='tutorials'),
    path('materials/publications', PublicationView.as_view(), name='publications'),

    path('f/<str:link>', LinkView.as_view(), name='short-file'),

    # Redirects from old url.
    path('programs', RedirectView.as_view(url='/abiturients/programs')),
    path('conferences', RedirectView.as_view(url='/about/conferences')),
    path('abiturients', RedirectView.as_view(url='/abiturients/info')),
    path('materials/timetable', RedirectView.as_view(url='/students/timetable')),
    path('materials/timetable/extramural', RedirectView.as_view(url='/students/timetable/extramural')),

    # TODO
    # Making registration backend by django-registration
    # path('auth/login', SmiapLoginView.as_view(), name='login'),
    # path('auth/logout', SmiapLogoutView.as_view(), name='logout'),
    # path('auth/register/', SmiapRegistrationView.as_view(), name='registration'),
    # path('auth/register/complete',
    #      TemplateView.as_view(template_name='auth/registration_complete.html'), name='registration_complete'),
    # path('auth/activate/<key:activation_key>/', SmiapActivationView.as_view(), name='activation'),
    # path('auth/complete',
    #      TemplateView.as_view(template_name='auth/activation_complete.html'), name='activation_complete'),
]
