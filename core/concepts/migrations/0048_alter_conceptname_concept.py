# Generated by Django 4.1.3 on 2023-01-18 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0047_auto_20230118_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conceptname',
            name='concept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='names', to='concepts.concept'),
        ),
    ]
