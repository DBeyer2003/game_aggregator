# Generated by Django 5.1.4 on 2025-01-06 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mockGameoMeter', '0004_gamescores_mock_mc_alter_gamescores_all_percent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamescores',
            name='critics_consensus',
            field=models.TextField(blank=True, null=True),
        ),
    ]
