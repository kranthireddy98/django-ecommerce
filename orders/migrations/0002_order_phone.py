# Generated by Django 5.0.1 on 2024-02-02 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]