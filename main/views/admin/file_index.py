from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import File


class SeveralPublicationsView(PermissionRequiredMixin, TemplateView):
    template_name = 'admin/publications/add_couple.html'
    permission_required = 'add_publication'
    render = {
        'opts': File._meta,
        'change': False,
        'is_popup': False,
        'save_as': True,
        'has_delete_permission': False,
        'has_add_permission': True,
        'has_change_permission': False,
        'add': True,
        'has_view_permission': True,
        'has_editable_inline_admin_formsets': True,
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.render)
