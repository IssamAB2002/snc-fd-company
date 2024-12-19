# Generated by Django 5.1.1 on 2024-12-14 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_code_expires_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email_verification_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_code_expires_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_verification_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
