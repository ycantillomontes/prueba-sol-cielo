from django.contrib import admin

from .models import PQRSAttachment, TicketPQRS


class PQRSAttachmentInline(admin.TabularInline):
    model = PQRSAttachment
    extra = 0
    can_delete = False
    readonly_fields = (
        "file",
        "uploaded_at",
    )

    fields = (
        "file",
        "uploaded_at",
    )

    def has_add_permission(self, request, obj=None):
        return False


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

    inlines = [
        PQRSAttachmentInline,
    ]