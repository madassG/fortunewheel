# Generated by Django 4.0.4 on 2022-05-31 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0013_wins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='probability',
            field=models.FloatField(default=0.1),
        ),
    ]