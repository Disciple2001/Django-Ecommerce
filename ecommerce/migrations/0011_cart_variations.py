# Generated by Django 5.1.1 on 2024-10-03 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_rename_product_variation_productvariation'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='variations',
            field=models.ManyToManyField(blank=True, to='ecommerce.productvariation'),
        ),
    ]
