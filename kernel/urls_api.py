from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('book/', include('kernel.book.api.urls')),
    path('book/xml/', include('kernel.xml.api.urls')),
]
