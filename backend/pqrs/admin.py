from django.contrib import admin

from .models import TicketPQRS


@admin.register(TicketPQRS)
class TicketPQRSAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_code",
        "applicant_name",
        "applicant_email",
        "category",
        "subject",
        "status",
        "created_at",
    )

    list_filter = (
        "category",
        "status",
        "created_at",
    )

    search_fields = (
        "ticket_code",
        "applicant_name",
        "applicant_email",
        "subject",
    )

    readonly_fields = (
        "ticket_code",
        "created_at",
    )