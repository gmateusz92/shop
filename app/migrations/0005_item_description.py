# Generated by Django 4.1.3 on 2022-11-11 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='this is a decsrpition'),
            preserve_default=False,
        ),
    ]
