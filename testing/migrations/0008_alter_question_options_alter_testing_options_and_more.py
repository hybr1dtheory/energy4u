# Generated by Django 5.0.1 on 2024-03-06 20:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0007_alter_testing_test_time_testingquestion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['?']},
        ),
        migrations.AlterModelOptions(
            name='testing',
            options={'get_latest_by': 'test_datetime', 'ordering': ['-test_datetime']},
        ),
        migrations.RenameField(
            model_name='testing',
            old_name='test_time',
            new_name='test_duration',
        ),
        migrations.RemoveField(
            model_name='testing',
            name='test_date',
        ),
        migrations.AddField(
            model_name='testing',
            name='test_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
