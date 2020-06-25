from django.apps import apps
from django.contrib.auth.views import redirect_to_login
from django.contrib.flatpages.models import FlatPage
from django.http import HttpResponse
from django.urls import reverse

from main.utils.date import TeachTime
from main.views.flatpage_view import FlatPageView
from news.models import News
from schedule.models import Group
from schedule.views import date_block


class IndexView(FlatPageView):
    def get(self, request, *args, **kwargs):
        if super()._not_authorized():
            return redirect_to_login(self.request.path)
        super()._mark_safe()

        template = super()._get_template()
        teach_time = TeachTime()
        news: News = apps.get_model(app_label="news", model_name="News")
        important_message = FlatPage.objects.get(url=reverse("important-message"))

        content = template.render(
            {
                "flatpage": self.flatpage,
                "date_block": date_block(teach_time),
                "groups": Group.objects.only("name"),
                "latest_news": news.objects.filter(hidden=False).order_by("-date")[:4],
                "teach_state": teach_time.teach_state,
                "important_message": important_message.content,
            },
            request,
        )
        return HttpResponse(content)
