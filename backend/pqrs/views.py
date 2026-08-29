from rest_framework import generics
from rest_framework.parsers import JSONParser

from .models import TicketPQRS
from .serializers import TicketPQRSSerializer


class TicketPQRSCrearView(generics.CreateAPIView):
    queryset = TicketPQRS.objects.all()
    serializer_class = TicketPQRSSerializer
    parser_classes = [
        JSONParser,
    ]