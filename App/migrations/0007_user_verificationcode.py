# Generated by Django 4.0.4 on 2022-07-05 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_user_emailverified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='VerificationCode',
            field=models.CharField(default='', max_length=128),
        ),
    ]
