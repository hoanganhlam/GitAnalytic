# Generated by Django 3.0.5 on 2020-05-08 15:59

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0006_auto_20200508_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gituser',
            name='email',
        ),
        migrations.AddField(
            model_name='gituser',
            name='links',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
