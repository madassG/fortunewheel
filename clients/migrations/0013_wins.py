# Generated by Django 4.0.4 on 2022-05-31 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0012_client_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.reward')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.client')),
            ],
        ),
    ]