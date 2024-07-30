# Generated by Django 5.0.6 on 2024-07-30 18:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_user_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='artists',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True), blank=True, default=list, null=True, size=None, unique=True),
        ),
    ]
