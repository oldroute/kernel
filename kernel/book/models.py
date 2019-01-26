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


class Task(models.Model):

    source = models.ForeignKey(Source, verbose_name="Источник", on_delete=models.SET_NULL, null=True, blank=True)
    source_raw_id = models.CharField(verbose_name="Идентификатор в источнике", max_length=255, null=True, blank=True)
    page = models.ForeignKey(Page, verbose_name="Страница", on_delete=models.SET_NULL, null=True, blank=True)
    tests = JSONField(blank=True, null=True)

    show = models.BooleanField(verbose_name="отображать", default=False)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)
    title = models.CharField(max_length=255, verbose_name="заголовок")
    slug = models.SlugField(verbose_name="слаг", max_length=255)
    author = models.ForeignKey(UserModel, verbose_name="Автор", on_delete=models.SET_NULL, blank=True, null=True)

    body = JSONField(blank=True, null=True)

    def __str__(self):
        return self.title
