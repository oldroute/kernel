from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from mptt.models import MPTTModel, TreeForeignKey


UserModel = get_user_model()


class Source(models.Model):

    class Meta:
        verbose_name = "источник"
        verbose_name_plural = "источники"

    name = models.CharField(verbose_name="наименование", max_length=255)

    def __str__(self):
        return self.name


class Page(MPTTModel):

    class Meta:
        ordering = ['lft']

    leaf = False
    parent = TreeForeignKey(
        'self', related_name='children',
        null=True, blank=True, editable=False, on_delete=models.CASCADE
    )

    show = models.BooleanField(verbose_name="отображать", default=False)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)
    title = models.CharField(max_length=255, verbose_name="заголовок")
    slug = models.SlugField(verbose_name="слаг", max_length=255)
    author = models.ForeignKey(UserModel, verbose_name="Автор", on_delete=models.SET_NULL, blank=True, null=True)

    body = JSONField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def children_exists(self):
        return self.get_children().exists()

    @property
    def tasks_exists(self):
        return self.tasks.all().exists()


    @property
    def short_data(self):
        return {
            "type": 'page',
            "show": self.show,
            "loaded": False,
            "text": self.title,
        }

    @property
    def full_data(self):
        return {
            "type": 'page',
            "show": self.show,
            "text": self.title,
            "loaded": True,
            "slug": self.slug,
            "body": self.body,
            "author": {
                "id": self.author.id,
                "full_name": self.author.get_full_name(),
             }
        }

    @property
    def children_short_data(self):
        return [{"text": ""}] if self.children_exists or self.tasks_exists else []

    @property
    def children_full_data(self):
        result = []
        for page in self.get_children():
            result.append({
                'id': page.id,
                'text': page.title,
                'children': [{"text": ""}] if page.children_exists or page.tasks_exists else [],
                'data': {
                    'type': 'page',
                    "show": page.show,
                    'text': page.title,
                    "loaded": False
                }
            })
        if self.tasks_exists:
            result.append({
                'id': self.id,
                'text': 'Задачи', 
                'children': [{"text": ""}],
                'data': {
                    'type': 'tasks',
                    'show': True,
                    "loaded": False
                }
            })
        return result


class Task(models.Model):

    source = models.ForeignKey(Source, verbose_name="Источник", on_delete=models.SET_NULL, null=True, blank=True)
    source_raw_id = models.CharField(verbose_name="Идентификатор в источнике", max_length=255, null=True, blank=True)
    page = models.ForeignKey(Page, related_name="tasks", verbose_name="Страница", on_delete=models.SET_NULL, null=True, blank=True)
    tests = JSONField(blank=True, null=True)

    show = models.BooleanField(verbose_name="отображать", default=False)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)
    title = models.CharField(max_length=255, verbose_name="заголовок")
    slug = models.SlugField(verbose_name="слаг", max_length=255)
    author = models.ForeignKey(UserModel, verbose_name="Автор", on_delete=models.SET_NULL, blank=True, null=True)

    body = JSONField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def short_data(self):
        return {
            "type": 'task',
            "show": self.show,
            "text": self.title,
            "loaded": False,
        }


    @property
    def full_data(self):
        return {
            "type": 'task',
            "show": self.show,
            "text": self.title,
            "loaded": False,
            "slug": self.slug,
            "body": self.body,
            "tests": self.tests,
            "author": {
                "id": self.author.id,
                "full_name": self.author.get_full_name(),
             }
        }
