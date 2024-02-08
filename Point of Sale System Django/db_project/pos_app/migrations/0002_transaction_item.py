# Generated by Django 4.2.7 on 2023-11-28 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pos_app.item')),
                ('transaction_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pos_app.transaction')),
            ],
        ),
    ]