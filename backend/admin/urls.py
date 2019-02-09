from django.urls import path
from .views import *

urlpatterns = [
    path('book/', book_admin),
]