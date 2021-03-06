# Generated by Django 3.2.8 on 2021-10-22 08:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211022_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_phone_num',
            field=models.CharField(max_length=13),
        ),
    ]
