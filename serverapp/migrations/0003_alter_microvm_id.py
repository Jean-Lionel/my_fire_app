# Generated by Django 5.0.6 on 2024-06-23 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverapp', '0002_remove_microvm_ip_remove_microvm_karnel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='microvm',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
