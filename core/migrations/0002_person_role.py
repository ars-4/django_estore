# Generated by Django 4.1.1 on 2023-04-05 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='role',
            field=models.CharField(default='customer', max_length=255, null=True),
        ),
    ]
