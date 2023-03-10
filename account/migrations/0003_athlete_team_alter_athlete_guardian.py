# Generated by Django 4.1.5 on 2023-01-28 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
        ('account', '0002_remove_athlete_age_alter_athlete_birthday_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='athlete',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='teams.teams'),
        ),
        migrations.AlterField(
            model_name='athlete',
            name='guardian',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
