from datetime import datetime

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import TemplateView

from main.forms import GetGroupScheduleForm
from main.management.scripts.generate import gen_groups_table
from main.models import FullTimeSchedule


class GetGroupScheduleXlsxView(TemplateView):
    template_name = 'admin/schedule/get_schedule.html'
    render = {
        'form': GetGroupScheduleForm(),
        'opts': FullTimeSchedule._meta,
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

    def post(self, request, *args, **kwargs):
        form = GetGroupScheduleForm(request.POST)
        if not form.is_valid():
            self.render.update({
                'form': form,
                'errors': form.errors,
                'opts': FullTimeSchedule._meta,
            })
            return render(request, self.template_name, self.render)

        groups = form.cleaned_data['groups']
        from_week = form.cleaned_data['from_week']
        filename = gen_groups_table(groups, from_week)
        try:
            with open(f'{filename}.xlsx', 'rb') as f:
                file_data = f.read()
            response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="{filename}_{date}.xlsx"'.format(
                filename=filename,
                date=datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            )
        except IOError:
            response = HttpResponseNotFound('<h1>File not exist</h1>')

        return response
