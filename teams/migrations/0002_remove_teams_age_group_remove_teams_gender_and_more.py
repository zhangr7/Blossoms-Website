# Generated by Django 4.1.5 on 2023-01-28 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teams',
            name='age_group',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='season',
        ),
        migrations.AddField(
            model_name='teams',
            name='group',
            field=models.CharField(default='Co-ed Spring23', max_length=50, verbose_name='Group'),
        ),
    ]
