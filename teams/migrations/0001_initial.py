# Generated by Django 4.1.5 on 2023-01-28 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_group', models.CharField(max_length=30, verbose_name='Age Group')),
                ('gender', models.CharField(max_length=50, verbose_name='Gender')),
                ('season', models.CharField(max_length=30, verbose_name='Season')),
            ],
        ),
    ]
