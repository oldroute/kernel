import os
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Import(models.Model):

    IMPORT_DIR = os.path.join(settings.UPLOAD_URL, 'xml')

    class Status:

        PROCESS = 0
        COMPLETE = 1
        ERROR = 2
        CHOICES = (
            (PROCESS, 'в процессе'),
            (COMPLETE, 'в завершен'),
            (ERROR, 'ошибка'),
        )

    class Messages:

        FAILURE = u'Ошибка чтения файла'
        SUCCESS = u'Успешный импорт файла'

    status = models.IntegerField(choices=Status.CHOICES, default=Status.PROCESS)
    date_start = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField(blank=True, null=True)
    file = models.FileField(upload_to=IMPORT_DIR)
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, blank=True, null=True)


class ImportLogItem(models.Model):

    event = models.ForeignKey(Import, on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=500)
    success = models.BooleanField(default=False)

