# Generated by Django 5.0.1 on 2024-01-21 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_rename_quatity_cartitem_quantity'),
        ('store', '0002_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
