# Generated by Django 4.1 on 2022-09-29 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YearMonthDay', '0010_rename_days_task_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='important',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='day',
            name='numberInt',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]