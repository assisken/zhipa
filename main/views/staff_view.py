from django.shortcuts import render
from django.views import View

from main.models import Staff


class StaffView(View):
    template_name = "about/staff.html"

    def get(self, request):
        staffs = Staff.objects.filter(hide=False)

        return render(
            request,
            self.template_name,
            {
                "leaders": filter(lambda staff: staff.leader, staffs),
                "lecturers": filter(lambda staff: not staff.leader, staffs),
            },
        )
