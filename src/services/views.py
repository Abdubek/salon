from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from salon.models import Salon
from services.models import Category, Service, ServiceMasters
from staffer.models import Staffer


class CategoryList(LoginRequiredMixin, ListView):
    model = Category


class CategoryCreate(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            title_kz = request.POST["title_kz"]
            title_ru = request.POST["title_ru"]
            gender = request.POST["gender"]

            new_category = Category(title_kz=title_kz, title_ru=title_ru, gender=gender)
            new_category.save()

            request.user.salon.service_categories.add(new_category)
            request.user.salon.save()

            return JsonResponse({"message": _("Сохранено")},
                                status=200)
        except Exception as e:
            return JsonResponse({"statusText": str(e)}, status=400)


class CategoryUpdate(LoginRequiredMixin, View):
    def post(self, request, cid, *args, **kwargs):
        try:
            category = get_object_or_404(Category, pk=cid)

            category.title_kz = request.POST["title_kz"]
            category.title_ru = request.POST["title_ru"]
            category.gender = request.POST["gender"]

            category.save()

            return JsonResponse({"message": _("Сохранено")},
                                status=200)
        except Exception as e:
            return JsonResponse({"statusText": str(e)}, status=400)


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('services:list-category')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['services'] = Service.objects.filter(category=category).all()

        return context


class ServiceCreate(LoginRequiredMixin, CreateView):
    model = Service
    fields = ('title_kz', 'title_ru', 'category', 'image', 'min_price', 'max_price', 'is_online')

    def form_valid(self, form):
        service = form.save(commit=False)
        service.manager = self.request.user
        service.save()

        return redirect(service.get_absolute_url())


class ServiceUpdate(LoginRequiredMixin, UpdateView):
    model = Service
    fields = ('title_kz', 'title_ru', 'category', 'image', 'min_price', 'max_price', 'is_online')


class ServiceDelete(LoginRequiredMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('services:list-category')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SalonServices(View):

    def get(self, request, sid, *args, **kwargs):
        try:
            data = {'categories': []}
            service_filter = {}
            master_id = int(request.GET.get('m_id', 0))

            if master_id:
                service_filter = {'master_id': master_id}

            salon = get_object_or_404(Salon, pk=sid)

            for category in salon.service_categories.all():
                service_filter['service__category'] = category
                services = ServiceMasters.objects.filter(**service_filter)

                info = {
                    'id': category.id,
                    'name': category.title_kz if request.LANGUAGE_CODE == 'kk' else category.title_ru,
                    'services': []
                }

                if not master_id:
                    services = services.distinct('service')

                for service in services:
                    info['services'].append({
                        'name': service.service.title_kz if request.LANGUAGE_CODE == 'kk' else service.service.title_ru,
                        'id': service.service.id,
                        'price': (service.service.max_price + service.service.min_price) // 2,
                        'duration': '%s:%s' % (service.duration_hours, service.duration_minutes)
                    })

                if info['services']:
                    data['categories'].append(info)

            return JsonResponse(data, status=200)
        except Exception as e:
            return JsonResponse({"statusText": str(e)}, status=400)
