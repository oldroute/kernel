from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import *


class BookRootView(generics.ListAPIView):

    permission_classes = [IsAdminUser]
    queryset = Page.objects.filter(level=0)
    serializer_class = PageRootSerializer


class PageDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdminUser]
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer


#class PageChildrenListView(generics.GenericAPIView):
#
#    permission_classes = [IsAdminUser]
#    queryset = Page.objects.all()
#    serializer_class = PageChildrenListSerializer
#
#    def get(self, request, *args, **kwargs):
#        queryset = self.filter_queryset(self.get_queryset()).filter(**kwargs)
#        serializer = self.get_serializer(queryset, many=True)
#        return Response(serializer.data)


class TaskListView(generics.GenericAPIView):

    permission_classes = [IsAdminUser]
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(**kwargs)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdminUser]
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
