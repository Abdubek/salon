from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from client.models import Client
from timetable.models import TimeTable


class ClientList(LoginRequiredMixin, ListView):
    model = Client


class ClientCreate(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('full_name', 'avatar', 'phone', 'email', 'gender', 'description')

    def form_valid(self, form):
        client = form.save(commit=False)

        client.salon = self.request.user.salon
        client.save()

        return redirect(client.get_absolute_url())


class ClientUpdate(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ('full_name', 'avatar', 'phone', 'email', 'gender', 'description')


class ClientDetail(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_object()

        histories = TimeTable.objects.filter(client=client)
        sum_profit = histories.aggregate(profit=Sum('amount'))
        count = histories.aggregate(services=Count('service_master__service'))

        context['histories'] = histories
        context['sum_profit'] = sum_profit
        context['count'] = count

        return context
