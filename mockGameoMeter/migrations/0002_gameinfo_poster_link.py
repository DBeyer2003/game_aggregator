# Generated by Django 5.1.4 on 2025-01-05 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mockGameoMeter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameinfo',
            name='poster_link',
            field=models.URLField(blank=True),
        ),
    ]
