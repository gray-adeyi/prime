# Generated by Django 4.0.3 on 2022-05-17 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_transaction_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
