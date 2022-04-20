# Generated by Django 4.0.3 on 2022-04-12 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collections', '0044_auto_20220406_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_related_created_by', related_query_name='%(app_label)s_%(class)ss_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='collection',
            name='updated_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_related_updated_by', related_query_name='%(app_label)s_%(class)ss_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='expansion',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_related_created_by', related_query_name='%(app_label)s_%(class)ss_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='expansion',
            name='updated_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_related_updated_by', related_query_name='%(app_label)s_%(class)ss_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]