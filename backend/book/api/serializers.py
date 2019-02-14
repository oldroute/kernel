from rest_framework import serializers
from backend.book.models import *
from django.forms.models import model_to_dict


class PageRootSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        exclude = ['lft', 'rght', 'tree_id', 'level', 'parent']

    meta = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    isLeaf = serializers.SerializerMethodField()

    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'name': obj.author.get_full_name()
        }

    def get_isLeaf(self, obj):
        return False if obj.get_children().exists() or obj.tasks.all().exists() else True

    def get_meta(self, obj):
        return {
            'class': obj.__class__.__name__.lower(),
        }


class PageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        exclude = ['lft', 'rght', 'tree_id', 'level', 'parent']

    meta = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()
    isLeaf = serializers.SerializerMethodField()

    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'name': obj.author.get_full_name()
        }

    def get_meta(self, obj):
        return {
            'class': obj.__class__.__name__.lower(),
        }

    def get_isLeaf(self, obj):
        return False if obj.get_children().exists() or obj.tasks.all().exists() else True

    def get_children(self, obj):
        result = list()
        for child in obj.get_children():
            data_dict = model_to_dict(child, exclude=['lft', 'rght', 'tree_id', 'level', 'parent', 'author'])
            data_dict['isLeaf'] = False if child.get_children().exists() or child.tasks.all().exists() else True
            data_dict['author'] = {
                'id': child.author.id,
                'name': child.author.get_full_name()
            }
            data_dict['meta'] = {
                'class': child.__class__.__name__.lower(),
            }
            result.append(data_dict)
        return result

    def get_tasks(self, obj):
        result = list()
        for task in obj.tasks.all():
            result.append(model_to_dict(task, exclude=['page']))
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

