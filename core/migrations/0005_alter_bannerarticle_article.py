# Generated by Django 5.1.1 on 2024-12-16 09:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_name_contactmessage_user'),
        ('shopping', '0009_alter_articleimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerarticle',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shopping.article'),
        ),
    ]