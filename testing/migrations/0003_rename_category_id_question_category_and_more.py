# Generated by Django 5.0.1 on 2024-01-28 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0002_question_reference'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='testing',
            old_name='category_id',
            new_name='category',
        ),
    ]