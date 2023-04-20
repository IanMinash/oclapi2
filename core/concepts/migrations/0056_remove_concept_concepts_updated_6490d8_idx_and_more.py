# Generated by Django 4.1.7 on 2023-04-05 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0055_remove_concept_concepts_updated_6490d8_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_updated_6490d8_idx',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_ver_sort_idx',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_public_conditional',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_ver_public',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_public_cond',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_all_for_count',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_ver_for_count',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_all_for_count2',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_all_for_sort',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_ver_for_sort',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_ver_updated_idx',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_ver_public_cond',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_ver_public_cond2',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_ver_all_for_count',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_ver_all_for_count2',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_ver_all_for_sort',
        ),
        migrations.RemoveIndex(
            model_name='concept',
            name='concepts_ver_all_for_sort_2',
        ),
        migrations.AddIndex(
            model_name='concept',
            index=models.Index(condition=models.Q(('is_active', True), ('retired', False)), fields=['-updated_at', 'public_access', 'is_latest_version'], name='concepts_up_pub_latest'),
        ),
        migrations.AddIndex(
            model_name='concept',
            index=models.Index(condition=models.Q(('is_active', True), ('retired', False), ('id', models.F('versioned_object_id'))), fields=['-updated_at', 'public_access', 'is_latest_version'], name='concepts_head_up_pub_latest'),
        ),
        migrations.AddIndex(
            model_name='concept',
            index=models.Index(condition=models.Q(('is_active', True), ('retired', False)), fields=['public_access', 'is_latest_version'], name='concepts_pub_latest'),
        ),
        migrations.AddIndex(
            model_name='concept',
            index=models.Index(condition=models.Q(('is_active', True), ('retired', False), ('id', models.F('versioned_object_id'))), fields=['public_access', 'is_latest_version'], name='concepts_head_pub_latest'),
        ),
        migrations.AddIndex(
            model_name='concept',
            index=models.Index(condition=models.Q(('is_active', True), ('retired', False)), fields=['is_latest_version', 'parent_id', 'public_access'], name='concepts_latest_parent_pub'),
        ),
        migrations.AddIndex(
            model_name='concept',
            index=models.Index(condition=models.Q(('is_active', True), ('retired', False)), fields=['-updated_at', 'is_latest_version'], name='concepts_up_latest'),
        ),
        migrations.AddIndex(
            model_name='concept',
            index=models.Index(condition=models.Q(('is_active', True), ('retired', False), ('id', models.F('versioned_object_id'))), fields=['parent_id', 'public_access'], name='concepts_head_parent_pub'),
        ),
    ]
