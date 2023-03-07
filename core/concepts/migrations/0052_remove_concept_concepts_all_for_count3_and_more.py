# Generated by Django 4.1.7 on 2023-03-03 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0051_concept_concepts_all_for_count3'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_all_for_count3',
        ),
        migrations.AddIndex(
            model_name='concept',
            index=models.Index(condition=models.Q(('is_active', True), ('retired', False), ('id', models.F('versioned_object_id'))), fields=['parent_id', '-updated_at', 'is_active', 'retired', 'id', 'versioned_object_id'], name='concepts_all_for_count3'),
        ),
    ]