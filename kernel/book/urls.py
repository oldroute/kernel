from django.urls import path, include
from .xml import urls as xml_urls


urlpatterns = [
    path('xml/', include(xml_urls))
]