from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include('backend.admin.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('backend.urls_api')),
]
