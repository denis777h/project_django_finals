# Generated by Django 4.2.11 on 2024-03-11 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pereval_data', '0003_alter_perevaladded_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perevaladded',
            name='level',
        ),
    ]
