from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('book/', include('backend.book.api.urls')),
    path('book/xml/', include('backend.xml.api.urls')),
]
