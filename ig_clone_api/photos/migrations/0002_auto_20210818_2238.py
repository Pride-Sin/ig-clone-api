# Generated by Django 3.1.13 on 2021-08-19 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='total_comments',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='photo',
            name='total_likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
