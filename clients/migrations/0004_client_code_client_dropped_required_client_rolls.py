# Generated by Django 4.0.4 on 2022-05-28 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_reward'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='code',
            field=models.CharField(default='gay', max_length=100),
        ),
        migrations.AddField(
            model_name='client',
            name='dropped_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='client',
            name='rolls',
            field=models.IntegerField(default=0),
        ),
    ]
