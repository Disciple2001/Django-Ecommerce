# Generated by Django 5.1.1 on 2024-10-08 11:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0013_alter_cart_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cart',
            new_name='CartItem',
        ),
    ]
