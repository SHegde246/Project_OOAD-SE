# Generated by Django 2.2.19 on 2021-04-03 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assimilate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='domain',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
