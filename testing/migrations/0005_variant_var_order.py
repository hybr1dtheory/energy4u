# Generated by Django 5.0.1 on 2024-02-21 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0004_rename_user_id_testing_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='var_order',
            field=models.CharField(max_length=1, null=True),
        ),
    ]