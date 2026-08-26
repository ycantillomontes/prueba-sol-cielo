from django.urls import path
from .views import TicketPQRSCrearView


urlpatterns = [
    path("", TicketPQRSCrearView.as_view(), name="crear-pqrs"),
]