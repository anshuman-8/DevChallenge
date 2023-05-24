# Generated by Django 4.2.1 on 2023-05-24 03:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hackathon',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('background_image', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=100)),
                ('reward', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('image', 'Image'), ('file', 'File'), ('link', 'Link')], default='image', editable=False, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('summary', models.TextField()),
                ('hackathon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HackSubmit.hackathon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
