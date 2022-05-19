# Generated by Django 4.0.3 on 2022-05-03 21:33

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_job_write_up_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(choices=[(0, '4x6'), (1, '5x7'), (2, '8x10')], default=1, max_length=2),
        ),
        migrations.AlterField(
            model_name='job',
            name='price_per_unit',
            field=models.DecimalField(decimal_places=2, default=Decimal('50'), max_digits=8),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[(0, 'booking'), (1, 'processing'), (2, 'completed')], default=0, max_length=2),
        ),
        migrations.AlterField(
            model_name='job',
            name='write_up',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
