# Generated by Django 3.1.12 on 2021-07-20 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collections', '0024_auto_20210716_1353'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='collection',
            index=models.Index(fields=['public_access'], name='collections_public__c15b3e_idx'),
        ),
    ]