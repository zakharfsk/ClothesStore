# Generated by Django 4.2.4 on 2023-08-26 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_basket'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basket',
            old_name='users',
            new_name='user',
        ),
    ]
