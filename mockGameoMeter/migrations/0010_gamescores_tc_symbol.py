# Generated by Django 5.1.4 on 2025-01-10 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mockGameoMeter', '0009_gamescores_all_symbol'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamescores',
            name='tc_symbol',
            field=models.CharField(blank=True, max_length=1),
        ),
    ]
