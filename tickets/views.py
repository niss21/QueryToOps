from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Ticket
from .serializers import TicketSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]  # 🔐 Only logged-in users

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # automatically sets creator