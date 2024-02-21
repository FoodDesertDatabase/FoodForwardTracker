# Generated by Django 4.1.3 on 2024-02-21 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fftracker', '0016_alter_recipes_r_servings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientunits',
            name='recipe_amt',
            field=models.DecimalField(decimal_places=4, max_digits=8),
        ),
        migrations.AlterField(
            model_name='ingredientunits',
            name='shop_amt',
            field=models.DecimalField(decimal_places=4, max_digits=8),
        ),
    ]
