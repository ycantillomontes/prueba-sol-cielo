from rest_framework import generics

from .models import TicketPQRS
from .serializers import TicketPQRSSerializer


class TicketPQRSCrearView(generics.CreateAPIView):
    queryset = TicketPQRS.objects.all()
    serializer_class = TicketPQRSSerializer