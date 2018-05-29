from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import ListView, UpdateView, TemplateView, CreateView, DeleteView

from services.models import ServiceMasters, Service
from staffer.forms import StafferInfoForm
from staffer.models import Staffer, Position, StafferInfo


class StafferList(LoginRequiredMixin, ListView):
    model = Staffer


class StafferUpdate(LoginRequiredMixin, UpdateView):
    model = Staffer
    template_name_suffix = '_new'
    fields = ('full_name', 'avatar', 'position', 'specialization', 'master_fired', 'description')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staffer = self.get_object()
        staffer_info_form = StafferInfoForm()
        master_services = ServiceMasters.objects.filter(master=staffer)
        services = Service.objects.filter(category__in=self.request.user.salon.service_categories.all()).exclude(pk__in=master_services.values_list('id', flat=True))

        try:
            staffer_info = StafferInfo.objects.get(staffer=staffer)
            staffer_info_form = StafferInfoForm(None, instance=staffer_info)
        except:
            pass

        context['staffer_info_form'] = staffer_info_form
        context['master_services'] = master_services
        context['services'] = services

        return context


class StafferInfoCreate(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            info_form = StafferInfoForm(request.POST or None)

            if info_form.is_valid():
                info_form.save()
            else:
                return JsonResponse({"statusText": info_form.errors.as_text() }, status=400)

            return JsonResponse({"message": _("Сохранено")},
                                status=200)
        except Exception as e:
            return JsonResponse({"statusText": str(e)}, status=400)


class StafferCreate(LoginRequiredMixin, CreateView):
    model = Staffer
    template_name_suffix = '_new'
    fields = ('full_name', 'avatar', 'position', 'specialization', 'master_fired', 'description')

    def form_valid(self, form):
        staffer = form.save()

        self.request.user.salon.staffers.add(staffer)
        self.request.user.salon.save()

        return redirect(staffer.get_absolute_url())


class PositionView(LoginRequiredMixin, TemplateView):
    template_name = 'staffer/position.html'

    def post(self, request, *args, **kwargs):
        try:
            title = request.POST["title"]
            description = request.POST["description"]

            new_position = Position(title=title, description=description)
            new_position.save()

            request.user.salon.positions.add(new_position)
            request.user.salon.save()

            return JsonResponse({"message": _("Сохранено")},
                                status=200)
        except Exception as e:
            return JsonResponse({"statusText": str(e)}, status=400)


class StafferAddService(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            service = get_object_or_404(Service, pk=request.POST['service'])
            master = get_object_or_404(Staffer, pk=request.POST['master'])
            hour, minute = request.POST['duration'].split(':')
            duration = (int(hour) * 60) + int(minute)

            new_master_service = ServiceMasters(service=service, master=master, duration=duration)
            new_master_service.save()

            return JsonResponse({"message": _("Услуга успешно добавлен для мастера.")},
                                status=200)
        except Exception as e:
            return JsonResponse({"statusText": str(e)}, status=400)


class StafferDeleteService(LoginRequiredMixin, DeleteView):
    model = ServiceMasters
    success_url = reverse_lazy('staffer:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class PositionUpdate(UpdateView):
    model = Position
    fields = ('title', 'description')


class PositionDelete(LoginRequiredMixin, DeleteView):
    model = Position
    success_url = Position.get_absolute_url()

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class StafferDelete(LoginRequiredMixin, DeleteView):
    model = Staffer
    success_url = reverse_lazy('staffer:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
