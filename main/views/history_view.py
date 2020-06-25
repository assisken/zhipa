from django.contrib.auth.views import redirect_to_login
from django.contrib.flatpages.models import FlatPage
from django.http import HttpResponse
from django.urls import reverse

from main.views.flatpage_view import FlatPageView


class HistoryView(FlatPageView):
    available = [1, 2, 3, 4]

    def setup(self, request, *args, **kwargs) -> None:
        try:
            super().setup(request, *args, **kwargs)
        except FlatPage.DoesNotExist:
            url = reverse("history", kwargs={"number": 1})
            self.flatpage = FlatPage.objects.get(url=url)

    def get(self, request, number=1):
        if super()._not_authorized():
            return redirect_to_login(self.request.path)
        super()._mark_safe()

        template = super()._get_template()
        content = template.render(
            {"flatpage": self.flatpage, "current": number, "available": self.available},
            request,
        )
        return HttpResponse(content)
