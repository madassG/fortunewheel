# Generated by Django 4.0.4 on 2022-05-28 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_client_code_client_dropped_required_client_rolls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='code',
            field=models.CharField(max_length=100),
        ),
    ]
