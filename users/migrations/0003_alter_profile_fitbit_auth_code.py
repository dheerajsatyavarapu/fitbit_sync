# Generated by Django 4.2.4 on 2023-08-18 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_fitbit_auth_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='fitbit_auth_code',
            field=models.TextField(max_length=50, null=True),
        ),
    ]
