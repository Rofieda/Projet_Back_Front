# Generated by Django 5.0.2 on 2024-03-30 06:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('lmcs', '0002_encadrement_role_chercheur2'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chercheur',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='lmcs.chercheur'),
        ),
    ]
