# Generated by Django 3.2.16 on 2023-01-03 19:57

import app_models.enums
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app_models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('deleted', models.BooleanField()),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_models.repository')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('deleted', models.BooleanField()),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('created_at', models.DateField()),
                ('state', enumfields.fields.EnumField(enum=app_models.enums.MilestoneState, max_length=10)),
                ('milestone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_models.project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
