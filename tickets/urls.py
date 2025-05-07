# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, CommentViewSet
from rest_framework_nested import routers

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')

tickets_router = routers.NestedDefaultRouter(router, r'tickets', lookup='ticket')
tickets_router.register(r'comments', CommentViewSet, basename='ticket-comments')

urlpatterns = router.urls + tickets_router.urls

# urlpatterns = [
#     path('', include(router.urls)),
# ]
