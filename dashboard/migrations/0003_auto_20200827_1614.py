# Generated by Django 3.1 on 2020-08-27 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20200827_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='query_location',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='query',
            name='query_timestamp',
            field=models.DateTimeField(blank=True),
        ),
    ]