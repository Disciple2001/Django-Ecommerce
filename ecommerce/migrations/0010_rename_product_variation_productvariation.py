# Generated by Django 5.1.1 on 2024-10-02 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0009_alter_cart_options_product_variation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product_Variation',
            new_name='ProductVariation',
        ),
    ]
