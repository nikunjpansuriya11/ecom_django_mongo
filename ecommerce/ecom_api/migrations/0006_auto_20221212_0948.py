# Generated by Django 3.0.5 on 2022-12-12 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_api', '0005_auto_20221212_0936'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='user_id',
            new_name='user',
        ),
    ]
