# Generated by Django 5.0.2 on 2025-02-19 07:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
