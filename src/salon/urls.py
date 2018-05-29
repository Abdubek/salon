from django.urls import path

from .views import SalonCreate, SalonUpdate, SalonContact, SalonOnline, InvoiceOnline, SalonOnlineHistory

app_name = "salon"

urlpatterns = [
    path('add/', SalonCreate.as_view(), name="add"),
    path('<int:pk>/', SalonUpdate.as_view(), name="detail"),
    path('contact', SalonContact.as_view(), name="contact"),
    path('online/<int:salon_id>', SalonOnline.as_view(), name="online"),
    path('online/history/<int:salon_id>', SalonOnlineHistory.as_view(), name="online-history"),
    path('invoice/<int:pk>', InvoiceOnline.as_view(), name="invoice")
]
