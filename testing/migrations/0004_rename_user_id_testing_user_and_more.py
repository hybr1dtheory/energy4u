# Generated by Django 5.0.1 on 2024-01-28 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0003_rename_category_id_question_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testing',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='variant',
            old_name='question_id',
            new_name='question',
        ),
    ]
