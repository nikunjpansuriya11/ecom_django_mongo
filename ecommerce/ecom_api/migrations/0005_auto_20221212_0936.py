# Generated by Django 3.0.5 on 2022-12-12 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecom_api', '0004_auto_20221212_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]