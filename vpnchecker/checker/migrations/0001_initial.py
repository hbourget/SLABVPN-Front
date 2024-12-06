# Generated by Django 5.1.3 on 2024-12-06 10:12

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(unique=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(unique=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(unique=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='checker.country')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('location_type', models.CharField(choices=[('City', 'City'), ('Country', 'Country')], max_length=50)),
                ('location_id', models.UUIDField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servers', to='checker.provider')),
            ],
        ),
        migrations.CreateModel(
            name='OutIp',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ip', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='out_ips', to='checker.server')),
            ],
        ),
        migrations.CreateModel(
            name='InIp',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ip', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_ips', to='checker.server')),
            ],
        ),
    ]
