# Generated by Django 4.2.10 on 2024-08-20 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0004_alter_article_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='extra_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
