# Generated by Django 4.2.1 on 2023-05-25 13:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("HackSubmit", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hackathon",
            name="type",
            field=models.CharField(
                choices=[("image", "Image"), ("file", "File"), ("link", "Link")],
                max_length=10,
            ),
        ),
    ]
