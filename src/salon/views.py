import uuid
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView
from django.utils.translation import gettext as _

from client.models import Client
from salon.forms import SalonContactFrom
from salon.models import Salon, Contact
from services.models import Service, ServiceMasters
from staffer.models import Staffer
from timetable.models import TimeTable


class SalonCreate(LoginRequiredMixin, CreateView):
    model = Salon
    fields = ('full_name', 'city', 'logo')

    def form_valid(self, form):
        salon = form.save(commit=False)
        salon.leader = self.request.user
        salon.save()

        self.request.user.salon = salon
        self.request.user.save()

        return redirect(salon.get_absolute_url())


class SalonUpdate(LoginRequiredMixin, UpdateView):
    model = Salon
    fields = ('full_name', 'city', 'logo')
    template_name_suffix = '_info'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salon = self.get_object()

        contact = Contact.objects.filter(salon=salon).first()
        contact_form = SalonContactFrom(instance=contact)

        context['contact_form'] = contact_form

        return context


class SalonContact(UpdateView):
    model = Contact
    form_class = SalonContactFrom

    def get_object(self, queryset=None):
        obj, created = self.model.objects.get_or_create(salon=self.request.user.salon)

        return obj

    def form_valid(self, form):
        contact = form.save(commit=False)
        contact.salon = self.request.user.salon
        contact.save()

        return redirect(contact.get_absolute_url())


class SalonOnline(View):
    template_name = 'salon/online.html'

    def get(self, request, salon_id, *args, **kwargs):
        salon = get_object_or_404(Salon, pk=salon_id)

        context = {
            'salon': salon
        }

        return render(request, self.template_name, context=context)

    def post(self, request, salon_id, *args, **kwargs):
        try:
            salon = get_object_or_404(Salon, pk=salon_id)
            service = get_object_or_404(Service, pk=request.POST['service_id'])
            master = Staffer.objects.filter(pk=request.POST['staffer_id']).first()
            start_datetime = datetime.strptime(request.POST['start_datetime'], '%Y-%m-%d %H:%M')
            comment = request.POST.get('comment')
            device_uid = request.session.get('device_uid', 0)

            if 9 > start_datetime.hour > 20:
                return JsonResponse({'statusText': _(u'Выберите рабочий время c 09:00 - 20:00')}, status=400)

            if not master:
                masters = list(Staffer.objects.filter(servicemasters__service=service).values_list('id', flat=True))
                job_masters = TimeTable.objects.filter(salon=salon, start__lte=start_datetime, end__gte=start_datetime)\
                                               .values_list('service_master__master_id', flat=True)

                for m in set(list(job_masters)):
                    if m in masters:
                        masters.remove(m)

                if not masters:
                    return JsonResponse({'statusText': _(u'Нет свободных мастер в это время!!!')}, status=400)

                master = Staffer.objects.get(pk=masters[0])

            if TimeTable.objects.filter(salon=salon, start__lt=start_datetime, end__gt=start_datetime, service_master__master=master).exists():
                return JsonResponse({'statusText': _(u'Время занято другим клиентом!!!')}, status=400)

            new_client = {
                'full_name': request.POST.get('client_name'),
                'email': request.POST.get('client_email'),
                'phone': request.POST.get('client_phone'),
                'salon': salon
            }

            if int(request.POST.get('client_id', 0)):
                client = Client.objects.get(pk=request.POST['client_id'])
            else:
                client = Client(**new_client)
                client.save()

            service_master = ServiceMasters.objects.filter(master=master, service=service).first()
            end_datetime = start_datetime + timedelta(minutes=service_master.duration)
            amount = (service.min_price + service.max_price) // 2

            if not service_master:
                return JsonResponse({'statusText': _(u'Нет свободных мастеров в это время!!!')}, status=400)

            if device_uid == 0:
                device_uid = str(uuid.uuid4())
                request.session['device_uid'] = device_uid

            new_timetable = TimeTable(
                salon=salon,
                client=client,
                service_master=service_master,
                start=start_datetime,
                end=end_datetime,
                comment=comment,
                amount=amount,
                device_uid=device_uid,
                is_online=True
            )
            new_timetable.save()

            msg = _(u'Сеанс успешно добавлен. Номер заказа <strong>%04d</strong>' % new_timetable.id)

            messages.success(request, msg)

            return JsonResponse({
                'message': msg
            }, status=200)
        except Exception as e:
            return JsonResponse({'statusText': str(e)}, status=400)


class InvoiceOnline(DetailView):
    model = TimeTable
    template_name = 'salon/invoice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        time_table = self.get_object()

        contact = Contact.objects.filter(salon=time_table.salon).first()

        context['contact'] = contact
        context['salon'] = time_table.salon

        return context


class SalonOnlineHistory(View):
    template_name = 'salon/online-history.html'

    def get(self, request, salon_id, *args, **kwargs):
        salon = get_object_or_404(Salon, pk=salon_id)
        device_uid = request.session.get('device_uid', 0)
        histories = TimeTable.objects.filter(device_uid=device_uid).all()

        context = {
            'salon': salon,
            'histories': histories,
            'device_uid': device_uid
        }

        return render(request, self.template_name, context=context)
