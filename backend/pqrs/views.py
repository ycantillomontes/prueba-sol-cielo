from rest_framework import generics
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from .models import PQRSAttachment, TicketPQRS
from .serializers import TicketPQRSSerializer


class TicketPQRSCrearView(generics.CreateAPIView):
    queryset = TicketPQRS.objects.all()
    serializer_class = TicketPQRSSerializer
    parser_classes = [
        JSONParser,
        MultiPartParser,
        FormParser,
    ]

    def perform_create(self, serializer):
        ticket = serializer.save()

        for file in self.request.FILES.getlist("attachments"):
            PQRSAttachment.objects.create(
                ticket=ticket,
                file=file,
            )