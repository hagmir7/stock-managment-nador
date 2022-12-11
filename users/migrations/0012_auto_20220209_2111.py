# Generated by Django 3.2.9 on 2022-02-09 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0011_auto_20220209_1058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='facebook',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='github',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='instagram',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='twitter',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='web',
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook', models.CharField(blank=True, max_length=300, null=True)),
                ('instagram', models.CharField(blank=True, max_length=300, null=True)),
                ('twitter', models.CharField(blank=True, max_length=300, null=True)),
                ('github', models.CharField(blank=True, max_length=300, null=True)),
                ('web', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]