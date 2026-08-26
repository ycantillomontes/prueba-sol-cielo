from rest_framework import serializers

from .models import TicketPQRS


class TicketPQRSSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPQRS
        fields = [
            "ticket_code",
            "applicant_name",
            "applicant_email",
            "category",
            "subject",
            "description",
            "attachment",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "ticket_code",
            "status",
            "created_at",
        ]