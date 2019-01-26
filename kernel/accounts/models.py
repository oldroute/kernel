from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class User(AbstractUser):

    first_name = models.CharField('Имя', max_length=20, blank=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)

    avatar = models.ImageField(upload_to=settings.UPLOAD_URL, blank=True, null=True)
    avatar_100x100 = ImageSpecField(
        source='avatar', format='JPEG',
        processors=[ResizeToFill(100, 100), ],
        options={'quality': 70}
    )

    def __str__(self):
        return self.get_full_name() or self.email
