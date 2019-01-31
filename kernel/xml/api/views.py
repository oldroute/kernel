from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser
from .serializers import ImportSerializer
from kernel.xml.models import Import


class ImportViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    queryset = Import.objects.all()
    serializer_class = ImportSerializer
    permission_classes = [IsAdminUser]
