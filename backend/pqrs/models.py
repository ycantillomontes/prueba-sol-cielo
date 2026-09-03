from django.contrib.auth import get_user_model
from django.db import models, transaction


class TicketSequence(models.Model):
    last_number = models.PositiveIntegerField(default=1000)

    def __str__(self):
        return str(self.last_number)


class TicketPQRS(models.Model):
    CATEGORY_CHOICES = [
        ("PETICION", "Petición"),
        ("QUEJA", "Queja"),
        ("RECLAMO", "Reclamo"),
        ("SUGERENCIA", "Sugerencia"),
    ]

    STATUS_CHOICES = [
        ("NUEVO", "Nuevo"),
        ("EN_REVISION", "En revisión"),
        ("RESUELTO", "Resuelto"),
        ("CERRADO", "Cerrado"),
    ]

    ticket_code = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )
    applicant_name = models.CharField(max_length=150)
    applicant_email = models.EmailField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="NUEVO",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.ticket_code:
            with transaction.atomic():
                sequence, _ = TicketSequence.objects.select_for_update().get_or_create(
                    pk=1,
                    defaults={"last_number": 1000},
                )
                sequence.last_number += 1
                sequence.save(update_fields=["last_number"])
                self.ticket_code = f"PQRS-{sequence.last_number}"
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_code} - {self.subject}"


class PQRSAttachment(models.Model):
    ticket = models.ForeignKey(
        TicketPQRS,
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    original_name = models.CharField(max_length=255)
    file = models.FileField(upload_to="pqrs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class TicketLog(models.Model):
    ticket = models.ForeignKey(
        TicketPQRS,
        on_delete=models.CASCADE,
        related_name="logs",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pqrs_logs",
    )
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ticket.ticket_code} - {self.created_at:%Y-%m-%d %H:%M}"
