# Generated by Django 5.0.3 on 2024-03-25 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0003_rename_task_task_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
