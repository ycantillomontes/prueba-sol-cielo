from rest_framework import serializers

from .models import PQRSAttachment, TicketPQRS


class PQRSAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PQRSAttachment
        fields = [
            "id",
            "file",
            "uploaded_at",
        ]
        read_only_fields = [
            "id",
            "uploaded_at",
        ]


class TicketPQRSSerializer(serializers.ModelSerializer):
    attachments = PQRSAttachmentSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = TicketPQRS
        fields = [
            "ticket_code",
            "applicant_name",
            "applicant_email",
            "category",
            "subject",
            "description",
            "status",
            "created_at",
            "attachments",
        ]
        read_only_fields = [
            "ticket_code",
            "status",
            "created_at",
            "attachments",
        ]