# Generated by Django 4.2.7 on 2023-12-02 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pos_app', '0002_transaction_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='payment',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
