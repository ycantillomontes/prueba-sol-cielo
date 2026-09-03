from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from rest_framework.parsers import JSONParser

from .models import PQRSAttachment, TicketLog, TicketPQRS
from .serializers import TicketPQRSSerializer


class TicketPQRSCrearView(generics.CreateAPIView):
    queryset = TicketPQRS.objects.all()
    serializer_class = TicketPQRSSerializer
    parser_classes = [JSONParser]

    def perform_create(self, serializer):
        serializer.save()


class TicketPQRSTRetrieveView(generics.RetrieveAPIView):
    queryset = TicketPQRS.objects.prefetch_related("attachments")
    serializer_class = TicketPQRSSerializer
    lookup_field = "ticket_code"
    lookup_url_kwarg = "ticket_code"


class PQRSLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class PQRSLogoutView(LogoutView):
    next_page = "gestion_login"


@login_required(login_url="gestion_login")
def gestion_dashboard(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    tickets = TicketPQRS.objects.all().order_by("-created_at")

    if query:
        tickets = tickets.filter(
            Q(ticket_code__icontains=query)
            | Q(applicant_name__icontains=query)
            | Q(applicant_email__icontains=query)
            | Q(subject__icontains=query)
        )

    if status:
        tickets = tickets.filter(status=status)

    paginator = Paginator(tickets, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "query": query,
        "selected_status": status,
        "status_choices": TicketPQRS.STATUS_CHOICES,
        "total_count": TicketPQRS.objects.count(),
        "new_count": TicketPQRS.objects.filter(status="NUEVO").count(),
        "review_count": TicketPQRS.objects.filter(status="EN_REVISION").count(),
        "resolved_count": TicketPQRS.objects.filter(status="RESUELTO").count(),
        "closed_count": TicketPQRS.objects.filter(status="CERRADO").count(),
    }
    return render(request, "pqrs/dashboard.html", context)


@login_required(login_url="gestion_login")
@require_http_methods(["GET", "POST"])
def gestion_ticket_detail(request, ticket_code):
    ticket = get_object_or_404(
        TicketPQRS.objects.prefetch_related("attachments", "logs__author"),
        ticket_code=ticket_code,
    )

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "status":
            new_status = request.POST.get("status")
            valid_statuses = {value for value, _ in TicketPQRS.STATUS_CHOICES}

            if new_status not in valid_statuses:
                messages.error(request, "El estado seleccionado no es válido.")
            elif new_status != ticket.status:
                old_status = ticket.get_status_display()
                ticket.status = new_status
                ticket.save(update_fields=["status"])

                TicketLog.objects.create(
                    ticket=ticket,
                    author=request.user,
                    note=(
                        f"Estado actualizado de «{old_status}» a "
                        f"«{ticket.get_status_display()}»."
                    ),
                )
                messages.success(request, "Estado actualizado correctamente.")
            else:
                messages.info(request, "El ticket ya tiene ese estado.")

        elif action == "note":
            note = request.POST.get("note", "").strip()
            if not note:
                messages.error(request, "Escribe una nota antes de guardarla.")
            elif len(note) > 2000:
                messages.error(request, "La nota no puede superar los 2000 caracteres.")
            else:
                TicketLog.objects.create(
                    ticket=ticket,
                    author=request.user,
                    note=note,
                )
                messages.success(request, "Nota agregada a la bitácora.")

        return redirect("gestion_ticket_detail", ticket_code=ticket.ticket_code)

    return render(
        request,
        "pqrs/ticket_detail.html",
        {
            "ticket": ticket,
            "status_choices": TicketPQRS.STATUS_CHOICES,
        },
    )
