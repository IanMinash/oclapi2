# Generated by Django 4.1.7 on 2023-04-13 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0060_auto_20230413_1130'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_public__932f92_idx',
        ),
    ]
