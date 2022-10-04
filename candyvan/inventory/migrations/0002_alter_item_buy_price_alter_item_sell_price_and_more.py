# Generated by Django 4.1.1 on 2022-10-02 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="buy_price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="item",
            name="sell_price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="revenue",
            name="revenue",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
