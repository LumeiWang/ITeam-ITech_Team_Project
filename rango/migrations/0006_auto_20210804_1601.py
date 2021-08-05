# Generated by Django 2.1.5 on 2021-08-04 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rango', '0005_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=256)),
            ],
        ),
        migrations.AlterField(
            model_name='page',
            name='url',
            field=models.URLField(unique=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rango.Page'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]