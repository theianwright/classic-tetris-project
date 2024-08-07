# Generated by Django 3.2.11 on 2024-07-08 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classic_tetris_project', '0078_auto_20240505_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pronouns',
            field=models.CharField(blank=True, choices=[('he', 'He/him/his'), ('she', 'She/her/hers'), ('they', 'They/them/theirs'), ('he/they', 'He/they'), ('they/he', 'They/he'), ('she/they', 'She/they'), ('they/she', 'They/she'), ('it', 'It/its'), ('xe', 'Xe/xem/xir'), ('any', 'Any/all'), ('ask', 'Ask')], max_length=16, null=True),
        ),
    ]
