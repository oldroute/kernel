from rest_framework import serializers
from kernel.book.models import *


class PageRootSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['id', 'text', 'data', 'children']

    text = serializers.CharField(source='title')
    data = serializers.ReadOnlyField(source='short_data')
    children = serializers.ReadOnlyField(source='children_short_data')


class PageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['id', 'text', 'data', 'children']

    text = serializers.CharField(source='title')
    data = serializers.ReadOnlyField(source='full_data')
    children = serializers.ReadOnlyField(source='children_full_data')


#class PageChildrenListSerializer(serializers.ModelSerializer):

#    class Meta:
#        model = Page
#        fields = ['id', 'text', 'data']


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'text', 'data']
   
    text = serializers.CharField(source='title')
    data = serializers.ReadOnlyField(source='short_data')


class TaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['id', 'text', 'data']

    text = serializers.CharField(source='title')
    data = serializers.ReadOnlyField(source='full_data')

