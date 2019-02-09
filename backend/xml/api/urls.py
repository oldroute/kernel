from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register('', ImportViewSet)

urlpatterns = [
    path('import/', include(router.urls))
]
