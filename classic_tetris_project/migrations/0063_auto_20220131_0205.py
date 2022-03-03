# Generated by Django 3.2.11 on 2022-01-31 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classic_tetris_project', '0062_auto_20220131_0118'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='tournamentplayer',
            name='unique_tournament_seed',
        ),
        migrations.AddIndex(
            model_name='tournamentplayer',
            index=models.Index(fields=['tournament', 'seed'], name='classic_tet_tournam_052ca2_idx'),
        ),
    ]