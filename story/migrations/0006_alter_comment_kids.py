# Generated by Django 3.2.5 on 2021-08-03 13:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0005_alter_story_kids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='kids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
    ]