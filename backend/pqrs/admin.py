from django.contrib import admin

from .models import PQRSAttachment, TicketLog, TicketPQRS


class PQRSAttachmentInline(admin.TabularInline):
    model = PQRSAttachment
    extra = 0
    can_delete = False
    readonly_fields = ("file", "uploaded_at")


class TicketLogInline(admin.TabularInline):
    model = TicketLog
    extra = 1
    fields = ("author", "note", "created_at")
    readonly_fields = ("author", "created_at")


@admin.register(TicketPQRS)
class TicketPQRSAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_code",
        "applicant_name",
        "category",
        "subject",
        "status",
        "created_at",
    )
    list_filter = ("status", "category")
    search_fields = (
        "ticket_code",
        "applicant_name",
        "applicant_email",
        "subject",
    )
    readonly_fields = ("ticket_code", "created_at")
    inlines = [PQRSAttachmentInline, TicketLogInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            if isinstance(instance, TicketLog) and not instance.author_id:
                instance.author = request.user
            instance.save()

        formset.save_m2m()