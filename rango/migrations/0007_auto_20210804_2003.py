# Generated by Django 2.1.5 on 2021-08-04 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rango', '0006_auto_20210804_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_title', models.CharField(max_length=32)),
                ('news_content', models.CharField(max_length=512)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='page',
        ),
        migrations.AddField(
            model_name='comment',
            name='newsID',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='pageID',
            field=models.IntegerField(null=True),
        ),
    ]