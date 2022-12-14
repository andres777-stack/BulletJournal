# Generated by Django 4.1 on 2022-10-06 00:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('YearMonthDay', '0004_goal_user_alter_goal_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='days', to='YearMonthDay.year'),
        ),
        migrations.RemoveField(
            model_name='year',
            name='user',
        ),
        migrations.AddField(
            model_name='year',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='years', to=settings.AUTH_USER_MODEL),
        ),
    ]
