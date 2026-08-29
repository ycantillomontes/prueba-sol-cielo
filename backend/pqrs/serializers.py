import base64
import binascii

from django.core.files.base import ContentFile
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
    attachments = serializers.SerializerMethodField()

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

    def to_internal_value(self, data):
        attachments = data.get("attachments", [])

        if attachments is None:
            attachments = []

        if not isinstance(attachments, list):
            raise serializers.ValidationError({
                "attachments": "Debe ser una lista de archivos."
            })

        validated_data = super().to_internal_value(data)

        validated_attachments = []

        for attachment in attachments:
            if not isinstance(attachment, dict):
                raise serializers.ValidationError({
                    "attachments": "Cada archivo debe ser un objeto."
                })

            name = attachment.get("name")
            content = attachment.get("content")

            if not name:
                raise serializers.ValidationError({
                    "attachments": "Cada archivo debe tener un nombre."
                })

            if not content:
                raise serializers.ValidationError({
                    "attachments": f"El archivo {name} no contiene información."
                })

            try:
                file_content = base64.b64decode(
                    content,
                    validate=True,
                )
            except (ValueError, TypeError, binascii.Error):
                raise serializers.ValidationError({
                    "attachments": f"El archivo {name} no contiene un Base64 válido."
                })

            validated_attachments.append(
                ContentFile(
                    file_content,
                    name=name,
                )
            )

        validated_data["_attachments"] = validated_attachments

        return validated_data

    def create(self, validated_data):
        attachments = validated_data.pop("_attachments", [])

        ticket = TicketPQRS.objects.create(**validated_data)

        for file in attachments:
            PQRSAttachment.objects.create(
                ticket=ticket,
                file=file,
            )

        return ticket

    def get_attachments(self, obj):
        return PQRSAttachmentSerializer(
            obj.attachments.all(),
            many=True,
        ).data