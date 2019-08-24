from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from main.models import Staff


class StaffView(LoginRequiredMixin, View):
    template_name = 'about/staff.html'
    login_url = reverse_lazy('login')

    def get(self, request):
        staffs = Staff.objects.filter(hide=False)

        return render(request, self.template_name, {
            'leaders': filter(lambda staff: staff.leader, staffs),
            'lecturers': filter(lambda staff: not staff.leader, staffs)
        })
