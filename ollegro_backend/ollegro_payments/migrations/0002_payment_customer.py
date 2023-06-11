# Generated by Django 4.2.1 on 2023-06-11 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ollegro_payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='customer',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.DO_NOTHING, related_name='purchases', to=settings.AUTH_USER_MODEL, verbose_name='Customer'),
            preserve_default=False,
        ),
    ]
