# Generated by Django 4.2.5 on 2023-10-12 18:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='teammates',
            field=models.ManyToManyField(related_name='teams', to=settings.AUTH_USER_MODEL),
        ),
    ]
