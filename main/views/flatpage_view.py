from django.contrib.auth.views import redirect_to_login
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.views import DEFAULT_TEMPLATE
from django.http import HttpResponse
from django.template import loader
from django.utils.safestring import mark_safe
from django.views.generic import View
from jinja2 import Template


class FlatPageView(View):
    flatpage: FlatPage

    def setup(self, request, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.flatpage = FlatPage.objects.get(url=request.path)

    def _not_authorized(self) -> bool:
        return (
            self.flatpage.registration_required
            and not self.request.user.is_authenticated
        )

    def _get_template(self) -> Template:
        if self.flatpage.template_name:
            return loader.select_template(
                [self.flatpage.template_name, DEFAULT_TEMPLATE]
            )
        else:
            return loader.get_template(DEFAULT_TEMPLATE)

    def _mark_safe(self) -> None:
        self.flatpage.title = mark_safe(self.flatpage.title)
        self.flatpage.content = mark_safe(self.flatpage.content)

    def get(self, request) -> HttpResponse:
        if self._not_authorized():
            return redirect_to_login(self.request.path)
        self._mark_safe()
        template = self._get_template()

        return HttpResponse(template.render({"flatpage": self.flatpage}, request))
