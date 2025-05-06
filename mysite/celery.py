import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketingSystem.settings')

app = Celery('ticketingSystem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()