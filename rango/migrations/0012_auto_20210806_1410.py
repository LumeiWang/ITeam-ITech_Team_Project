# Generated by Django 2.1.5 on 2021-08-06 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0011_page_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='categoryID',
        ),
        migrations.AddField(
            model_name='news',
            name='category',
            field=models.CharField(default='Python', max_length=512),
            preserve_default=False,
        ),
    ]
