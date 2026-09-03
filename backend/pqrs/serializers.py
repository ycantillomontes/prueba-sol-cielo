import base64
import binascii
import re

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import PQRSAttachment, TicketLog, TicketPQRS


MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_ATTACHMENTS = 5


class PQRSAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PQRSAttachment
        fields = ["id", "original_name", "file", "uploaded_at"]
        read_only_fields = ["id", "original_name", "file", "uploaded_at"]


class TicketPQRSSerializer(serializers.ModelSerializer):
    attachments = PQRSAttachmentSerializer(many=True, read_only=True)

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

    def validate(self, attrs):
        request = self.context.get("request")
        attachments = request.data.get("attachments", []) if request else []

        if attachments is None:
            attachments = []
        if not isinstance(attachments, list):
            raise serializers.ValidationError(
                {"attachments": "Debe ser una lista de documentos en formato JSON."}
            )

        if len(attachments) > MAX_ATTACHMENTS:
            raise serializers.ValidationError(
                {"attachments": f"Puedes adjuntar máximo {MAX_ATTACHMENTS} archivos."}
            )

        for item in attachments:
            if not isinstance(item, dict):
                raise serializers.ValidationError(
                    {"attachments": "Cada documento debe contener nombre y contenido."}
                )

            name = str(item.get("name", "")).strip()
            content = item.get("content")

            if not name.lower().endswith(".pdf"):
                raise serializers.ValidationError(
                    {"attachments": "Solo se permiten archivos PDF."}
                )

            if not isinstance(content, str) or not content:
                raise serializers.ValidationError(
                    {"attachments": f"El contenido de {name or 'el archivo'} no es válido."}
                )

            try:
                raw_content = content.split(",", 1)[-1]
                decoded = base64.b64decode(raw_content, validate=True)
            except (ValueError, binascii.Error):
                raise serializers.ValidationError(
                    {"attachments": f"El archivo {name} no contiene Base64 válido."}
                )

            if len(decoded) > MAX_FILE_SIZE:
                raise serializers.ValidationError(
                    {"attachments": f"Cada archivo PDF debe pesar máximo 5 MB: {name}."}
                )

            if not decoded.startswith(b"%PDF"):
                raise serializers.ValidationError(
                    {"attachments": f"El archivo {name} no parece ser un PDF válido."}
                )

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        attachments = request.data.get("attachments", []) if request else []
        ticket = TicketPQRS.objects.create(**validated_data)

        TicketLog.objects.create(
          ticket=ticket,
          author=None,
          note="PQRS radicada correctamente.",
        )

        for item in attachments or []:
          original_name = re.sub(r"[^A-Za-z0-9._-]", "_", str(item["name"]).strip())
          raw_content = item["content"].split(",", 1)[-1]
          decoded = base64.b64decode(raw_content, validate=True)
          attachment = PQRSAttachment(ticket=ticket, original_name=original_name)
          attachment.file.save(original_name, ContentFile(decoded), save=True)

        return ticket
