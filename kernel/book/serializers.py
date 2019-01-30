from rest_framework import serializers
from .models import *


class PageRootSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['id', 'show', 'title']


class PageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        exclude = ['lft', 'rght', 'tree_id', 'level', 'parent']
        read_only_fields = ['id', 'author', 'last_modified']


class PageChildrenListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['id', 'show', 'title']


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'show', 'title']


class TaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        exclude = ['page']
        read_only_fields = ['id', 'author', 'last_modified']

