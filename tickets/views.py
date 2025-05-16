from rest_framework import filters 
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket
from .serializers import TicketSerializer
from .permissions import IsCreatorOrAssignee
from rest_framework.permissions import IsAuthenticated  
from .serializers import CommentSerializer
from .models import Comment
from rest_framework.exceptions import PermissionDenied
from django.db import models


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]  # 🔐 Only logged-in users


    filterset_fields = {
    'created_at': ['gte', 'lte'],  # ⬅️ allow filtering by date range
    'status': ['exact'],
    'assigned_to': ['exact'],
    'category': ['exact'],
}  # Filter by these fields
    search_fields = ['title', 'description']      # Enable search by text

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsCreatorOrAssignee()]
        return super().get_permissions()
    

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # automatically sets creator

    # def get_queryset(self):
    #     # Only tickets created by this user
    #     return Ticket.objects.filter(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(
            models.Q(created_by=user) | models.Q(assigned_to=user)
        ).distinct()


    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def assigned(self, request):
        user = request.user
        tickets = Ticket.objects.filter(assigned_to=user)
        page = self.paginate_queryset(tickets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,  # 👈 Enable ordering
    ]
    ordering_fields = ['created_at', 'status', 'title']  # 👈 Allowed fields to order by
    ordering = ['-created_at']  # 👈 Default ordering

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(ticket__id=self.kwargs['ticket_pk'])

    def perform_create(self, serializer):
        ticket_id = self.kwargs['ticket_pk']
        ticket = Ticket.objects.get(pk=ticket_id)
        user = self.request.user

        # Only creator or assigned users can comment
        if ticket.created_by != user and user not in ticket.assigned_to.all():
            raise PermissionDenied("You are not allowed to comment on this ticket.")

        serializer.save(author=user, ticket=ticket)