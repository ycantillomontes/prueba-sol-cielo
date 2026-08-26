from django.db import models


class TicketPQRS(models.Model):
    CATEGORY_CHOICES = [
        ("PETICION", "Petición"),
        ("QUEJA", "Queja"),
        ("RECLAMO", "Reclamo"),
        ("SUGERENCIA", "Sugerencia"),
    ]

    STATUS_CHOICES = [
        ("NUEVO", "Nuevo"),
        ("EN_REVISION", "En Revisión"),
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

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
    )

    subject = models.CharField(max_length=200)

    description = models.TextField()

    attachment = models.FileField(
        upload_to="pqrs/",
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="NUEVO",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.ticket_code:
            last_ticket = (
                TicketPQRS.objects
                .order_by("-id")
                .first()
            )

            next_number = 1001 if not last_ticket else last_ticket.id + 1001

            self.ticket_code = f"PQRS-{next_number}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_code} - {self.subject}"