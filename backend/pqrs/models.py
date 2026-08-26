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

    def __str__(self):
        return f"{self.ticket_code} - {self.subject}"