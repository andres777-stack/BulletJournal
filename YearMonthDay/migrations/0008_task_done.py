# Generated by Django 4.1 on 2022-09-07 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YearMonthDay', '0007_alter_task_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
