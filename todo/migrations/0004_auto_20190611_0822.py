# Generated by Django 2.0.13 on 2019-06-11 08:22

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_auto_20190611_0810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='name',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.UserProfile'),
        ),
        migrations.AlterField(
            model_name='task',
            name='acomplish_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 12, 8, 22, 15, 904386, tzinfo=utc)),
        ),
    ]