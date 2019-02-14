from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from mptt.models import MPTTModel, TreeForeignKey


UserModel = get_user_model()


class Source(models.Model):

    class Meta:
        verbose_name = 'источник'
        verbose_name_plural = 'источники'

    name = models.CharField(verbose_name='наименование', max_length=255)

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

    show = models.BooleanField(verbose_name='отображать', default=False)
    last_modified = models.DateTimeField(verbose_name='дата последнего изменения', auto_now=True)
    title = models.CharField(max_length=255, verbose_name='заголовок')
    slug = models.SlugField(verbose_name='слаг', max_length=255)
    author = models.ForeignKey(UserModel, verbose_name='Автор', on_delete=models.SET_NULL, blank=True, null=True)

    body = JSONField(blank=True, null=True)

    def __str__(self):
        return self.title


class Task(models.Model):

    class Meta:
        ordering = ['order_key']

    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)
    source_raw_id = models.CharField(max_length=255, null=True, blank=True)
    page = models.ForeignKey(Page, related_name='tasks', on_delete=models.SET_NULL, null=True, blank=True)
    tests = JSONField(blank=True, null=True)

    show = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, blank=True, null=True)
    order_key = models.IntegerField(default=-1)
    body = JSONField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.order_key < 0:
            self.order_key = self.page.tasks.all().aggregate(models.Max('order_key'))['order_key__max'] + 1
        super(Task, self).save(args, kwargs)

    # def get_data(self, mode='short'):
    #     if mode == 'short':
    #         data = model_to_dict(self, exclude=['id', 'tests'])
    #     elif mode == 'full':
    #         data = model_to_dict(self, exclude=['id'])
    #     data['author'] = {'name': self.author.__str__(), 'id': self.author.id}
    #     data['class'] = self.__class__.__name__.lower()
    #     # data['loaded'] = False
    #     data['tests_exists'] = bool(self.tests)
    #     return data
