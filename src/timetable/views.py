from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _

from django.views import View

from client.models import Client
from salon.models import Salon
from services.models import Service, ServiceMasters
from staffer.models import Staffer
from timetable.models import TimeTable
from django.utils import timezone

from datetime import datetime, timedelta
from pytz import timezone as set_timezone


class TimeTableNew(LoginRequiredMixin, View):
    template_name = 'salon/new_session.html'

    def get(self, request, sid, *args, **kwargs):
        salon = get_object_or_404(Salon, pk=sid)
        clients = Client.objects.filter(salon=salon).all()

        context = {
            'salon': salon,
            'clients': clients
        }

        return render(request, self.template_name, context=context)

    def post(self, request, sid, *args, **kwargs):
        try:
            salon = get_object_or_404(Salon, pk=sid)
            service = get_object_or_404(Service, pk=request.POST['service_id'])
            master = Staffer.objects.filter(pk=request.POST['staffer_id']).first()
            start_datetime = datetime.strptime(request.POST['start_datetime'], '%Y-%m-%d %H:%M')
            comment = request.POST.get('comment')

            if 9 > start_datetime.hour > 20:
                return JsonResponse({'statusText': _(u'Выберите рабочий время c 09:00 - 20:00')}, status=400)

            if not master:
                masters = list(Staffer.objects.filter(servicemasters__service=service).values_list('id', flat=True))
                job_masters = TimeTable.objects.filter(salon=salon, start__lte=start_datetime, end__gte=start_datetime, service_master__service=service)\
                                               .values_list('service_master__master_id', flat=True)

                for m in set(list(job_masters)):
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

            if int(request.POST['client_id']):
                client = Client.objects.get(pk=request.POST['client_id'])
            else:
                client = Client(**new_client)
                client.save()

            service_master = ServiceMasters.objects.filter(master=master, service=service).first()
            end_datetime = start_datetime + timedelta(minutes=service_master.duration)
            amount = (service.min_price + service.max_price) // 2

            new_timetable = TimeTable(
                salon=salon,
                client=client,
                service_master=service_master,
                manager=request.user,
                start=start_datetime,
                end=end_datetime,
                comment=comment,
                amount=amount
            )
            new_timetable.save()

            return JsonResponse({'message': _(u'Сеанс успешно добавлен.')}, status=200)
        except Exception as e:
            return JsonResponse({'statusText': str(e)}, status=400)


class TimeTableList(View):

    def get(self, request, sid, *args, **kwargs):
        try:
            salon = get_object_or_404(Salon, pk=sid)
            master_id = request.GET.get('m_id')
            service_id = request.GET.get('s_id')

            time_list = TimeTable.objects.filter(
                salon=salon,
                start__gte=timezone.now(),
                service_master__service_id=service_id
            )

            if master_id:
                time_list = time_list.filter(service_master__master_id=master_id)

            context = {
                'disabled_dates': list(map(lambda x: x.start.isoformat(), time_list)),
                'locale': request.LANGUAGE_CODE,
                'startDate': timezone.now().isoformat()
            }

            return JsonResponse(context, status=200)
        except Exception as e:
            return JsonResponse({'statusText': str(e)}, status=400)


class TimeTableMain(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            str_time = "Уақыт: %s" if request.LANGUAGE_CODE == 'kk' else "Время: %s"
            localtz = set_timezone("Asia/Almaty")

            start_date = datetime.fromtimestamp(int(request.GET['start']))
            end_date = datetime.fromtimestamp(int(request.GET['end']))

            timetables = TimeTable.objects.filter(
                salon=request.user.salon,
                start__date__gte=start_date,
                end__date__lte=end_date
            )
            context = {
                'timetables': list(map(lambda x: {
                    'id': x.id,
                    'title': x.service_master.service.title_kz if request.LANGUAGE_CODE == 'kk' else x.service_master.service.title_ru,
                    'start': x.start.isoformat(),
                    'end': x.end.isoformat(),
                    'description': "<br>".join(["Клиент: %s" % x.client.full_name, "Мастер: %s" % x.service_master.master.full_name, str_time % x.start.strftime('%d.%m.%Y %H:%M'), x.comment])
                }, timetables)),
            }

            return JsonResponse(context, status=200)
        except Exception as e:
            raise
            return JsonResponse({'statusText': str(e)}, status=400)
