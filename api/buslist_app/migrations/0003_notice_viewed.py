# Generated by Django 5.1.1 on 2024-11-02 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buslist_app", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="notice",
            name="viewed",
            field=models.BooleanField(default=False),
        ),
    ]
