# Generated by Django 5.0.6 on 2024-07-30 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_avatar_url_user_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
