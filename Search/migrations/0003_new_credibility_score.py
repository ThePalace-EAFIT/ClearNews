# Generated by Django 5.0.2 on 2025-02-19 08:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0002_alter_new_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='new',
            name='credibility_score',
            field=models.IntegerField(default=50, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
