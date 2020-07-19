# Generated by Django 3.0.7 on 2020-07-19 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_auto_20200718_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content',
        ),
        migrations.AddField(
            model_name='post',
            name='content_delta',
            field=models.CharField(default='old posts', max_length=1000),
        ),
        migrations.AlterField(
            model_name='post',
            name='content_html',
            field=models.CharField(default='old posts', max_length=2000),
        ),
    ]
