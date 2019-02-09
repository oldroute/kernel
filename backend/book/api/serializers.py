from rest_framework import serializers
from backend.book.models import *


class PageRootSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['id', 'data']

    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        return obj.get_data()


class PageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['id', 'data', 'children', 'tasks']

    data = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    def get_data(self, obj):
        return obj.get_data()

    def get_children(self, obj):
        result = list()
        for child in obj.get_children():
            result.append({
                'id': child.id,
                'data': child.get_data(),
            })
        return result

    def get_tasks(self, obj):
        result = list()
        for task in obj.tasks.all():
            result.append({
                'id': task.id,
                'data': task.get_data(mode='short'),
            })
        return result


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'data']
   
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        return obj.get_data()


class TaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'data']

    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        return obj.get_data(mode='full')

