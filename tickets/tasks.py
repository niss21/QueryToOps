from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Ticket

@shared_task
def auto_extend_old_tickets():
    threshold_date = timezone.now() - timedelta(days=3)
    old_tickets = Ticket.objects.filter(status='active', created_at__lt=threshold_date)
    count = old_tickets.update(status='extended')
    return f"{count} tickets updated to 'extended'"