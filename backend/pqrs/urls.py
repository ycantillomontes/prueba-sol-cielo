from django.urls import path

from .views import (
    PQRSLoginView,
    PQRSLogoutView,
    TicketPQRSCrearView,
    TicketPQRSTRetrieveView,
    gestion_dashboard,
    gestion_ticket_detail,
)

urlpatterns = [
    # Panel interno MVT
    path("gestion/login/", PQRSLoginView.as_view(), name="gestion_login"),
    path("gestion/logout/", PQRSLogoutView.as_view(), name="gestion_logout"),
    path("gestion/", gestion_dashboard, name="gestion_dashboard"),
    path(
        "gestion/ticket/<str:ticket_code>/",
        gestion_ticket_detail,
        name="gestion_ticket_detail",
    ),

    # API pública para Next.js
    path("", TicketPQRSCrearView.as_view(), name="crear-pqrs"),
    path(
        "<str:ticket_code>/",
        TicketPQRSTRetrieveView.as_view(),
        name="consultar-pqrs",
    ),
]