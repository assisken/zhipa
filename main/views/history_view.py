from django.shortcuts import render
from django.views import View


class HistoryView(View):
    def get(self, request, number=1):
        available = [1, 2, 3, 4]

        return render(request, f'about/history/history_{number}.html', {
            'current': number,
            'available': available
        })
