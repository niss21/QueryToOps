from rest_framework import serializers
from .models import Comment
from .models import Ticket
from django.contrib.auth import get_user_model

User = get_user_model()

class TicketSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'image', 'description', 'status', 'assigned_to', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        assigned_users = validated_data.pop('assigned_to')
        ticket = Ticket.objects.create(created_by=self.context['request'].user, **validated_data)
        ticket.assigned_to.set(assigned_users)
        return ticket

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = ['id', 'ticket', 'author', 'text', 'created_at']
        read_only_fields = ['id', 'created_at', 'author']