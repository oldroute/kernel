# Generated by Django 2.1.5 on 2019-02-09 07:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_auto_20190131_2026'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['order_key']},
        ),
        migrations.AddField(
            model_name='task',
            name='order_key',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='book.Page'),
        ),
        migrations.AlterField(
            model_name='task',
            name='show',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
        migrations.AlterField(
            model_name='task',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.Source'),
        ),
        migrations.AlterField(
            model_name='task',
            name='source_raw_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
