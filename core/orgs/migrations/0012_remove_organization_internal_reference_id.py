# Generated by Django 3.2.7 on 2021-09-14 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0011_auto_20210914_0349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='internal_reference_id',
        ),
    ]
