# Generated by Django 5.0.2 on 2024-03-31 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lmcs', '0002_encadrement_role_chercheur2'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='publication',
            unique_together=set(),
        ),
    ]
